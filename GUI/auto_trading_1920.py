import jwt
import uuid
import hashlib
import os
from urllib.parse import urlencode
import requests
import time
import datetime as dt

from PyQt5.QtCore import QTimer, Qt, QThread
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem,QCompleter
from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
access_key = ''
secret_key = ''
user_email = ''
import PyQt5.QtWebEngineWidgets

#멀티스레딩
class Worker(QThread):
    def __init__(self):
        super().__init__()
        self.now_coin = ''
        self.running = False

    def get_day_candle(self, time):
        # 기준일-1 부터 n일까지의 일봉 요청
        time = dt.datetime(time.year, time.month, time.day, 0, 0, 0)
        url = "https://api.upbit.com/v1/candles/days"
        headers = {"Accept": "application/json"}
        querystring = {"market": 'KRW-'+self.now_coin,
                       "count": 30,
                       "to": time
                       }
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response.json()

    def get_30min_candle(self, time):
        time = dt.datetime(time.year, time.month, time.day, 0, 0, 0) + dt.timedelta(days=1)
        url = "https://api.upbit.com/v1/candles/minutes/30"
        headers = {"Accept": "application/json"}
        querystring = {"market": 'KRW-'+self.now_coin,
                       "count": 48,
                       "to": time
                       }
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response.json()

    def compute_k(self, coin_day_candle):
        # utc 최근 20일간의 noise ratio 평균
        response = coin_day_candle
        k = 0
        for i in response:
            k += 1 - abs(i["opening_price"] - i["trade_price"]) / (i["high_price"] - i["low_price"])
        return k / 20

    def compute_range(self, coin_day_candle):
        # 전날 (고가) - (저가)
        return coin_day_candle[0]['high_price'] - coin_day_candle[0]['low_price']
    def coin_trade(self, b_s, my_money, target_money):
        quantity = 0
        if b_s == 1:
            #sell 주문 시 팔려는 수량 갖고 오기
            payload = {
                'access_key': access_key,
                'nonce': str(uuid.uuid4()),
            }

            jwt_token = jwt.encode(payload, secret_key)
            authorize_token = 'Bearer {}'.format(jwt_token)
            headers = {"Authorization": authorize_token}

            res = requests.get("https://api.upbit.com/v1/accounts", headers=headers)
            for i in res.json():
                if i['currency'] == 'KRW-' + self.now_coin:
                    quantity = i['balance']
        else :
            quantity = target_money/my_money
        # 종가가 목표가 이상이면 구매
        query = {
            'market': 'KRW-' + self.now_coin,
            'side': ['bid', 'ask'][b_s],
            'volume': quantity,
            'price': target_money,
            'ord_type': 'limit',
        }
        query_string = urlencode(query).encode()

        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }

        jwt_token = jwt.encode(payload, secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.post("https://api.upbit.com/v1/orders", params=query, headers=headers)
        res = res.json()
    def run(self):
        time_tmp = ''
        target_price = 0
        trade_chk = 0
        while self.running:#
            min30_candle = self.get_30min_candle(dt.datetime.utcnow())
            print(time_tmp, min30_candle)
            if min30_candle[0]['candle_date_time_utc'][-8:] == '00:00:00' or time_tmp == '':
                #최초 실행 or 00시 갱신, 주문 냈으면 종가에 전량 매도.
                day_candle = self.get_day_candle(dt.datetime.utcnow())
                c_k = self.compute_k(day_candle)
                rng = self.compute_range(day_candle)
                target_price = (day_candle[0]['opening_price'] + c_k * rng) // 1000 * 1000
                if trade_chk == 1:
                    self.coin_trade(1, self.money, min30_candle[1]['trade_price'])
                    trade_chk = 0

            if target_price == 0 and min30_candle[1]['candle_date_time_utc'] != time_tmp:
                #30분마다 종가 체크, 목표가 달성시 매수 주문
                time_tmp = min30_candle[1]['candle_date_time_utc']
                if min30_candle[1]['trade_price'] >= target_price:
                    self.coin_trade(0, self.money, target_price)
                    trade_chk = 1

            time.sleep(1/15)

    def resume(self, nc, mon):
        self.running = True
        self.now_coin = nc
        self.money = mon
    def pause(self):
        self.running = False
    def test_(self, nc, t, end_day_):
        test_money = 1
        self.now_coin = nc
        while t < end_day_:
            day_candle = self.get_day_candle(t)
            min_candle = self.get_30min_candle(t)
            c_k = self.compute_k(day_candle)
            rng = self.compute_range(day_candle)
            target_price = (min_candle[-1]['opening_price'] + c_k * rng) // 1000 * 1000
            sell_price = 0
            chk = 0
            chk_trade = 0
            loss_cut_chk = 0
            # 만약 30분봉 종가가 목표가 이상이면, 거래
            # if min_candle[-1]['candle_date_time_utc'].split('T')[1] == '00:00:00':
            for j in range(47, -1, -1):
                if chk == 1 and chk_trade == 0 and (min_candle[j]['low_price'] < target_price):
                    chk_trade = 1
                if chk == 0 and min_candle[j]['trade_price'] >= target_price:
                    chk = 1
                # if chk_trade == 1 and min_candle[j]['trade_price'] < target_price * (1-0.02/scma):
                if chk_trade == 1 and min_candle[j]['trade_price'] < target_price*0.97:
                    loss_cut_chk = 1
                    sell_price = min_candle[j]['trade_price']
                    break

            if chk_trade == 1:
                if loss_cut_chk == 0:
                    sell_price = min_candle[0]['trade_price']
                # real_yield = (1-scma) + scma*((sell_price / target_price - 1.001) + 1)
                real_yield = sell_price / target_price - 0.001
                test_money *= real_yield
            t += dt.timedelta(days=1)
            time.sleep(1 / 20)
        return test_money


#pyqt
class Ui_MainWindow(object):
    def coin_change(self):
        if not (self.edit_search.text() in self.coin_list):
            self.edit_search.setText('비트코인/BTC')
        tmp = self.edit_search.text()
        tmp = tmp.split('/')[1]
        self.now_coin = tmp
        self.webEngineView.setUrl(PyQt5.QtCore.QUrl("https://upbit.com/full_chart?code=CRIX.UPBIT.KRW-"+self.now_coin))


    def test_button(self):
        self._yield.show()
        self._yield.setText('수익률 계산중...')
        self._yield.repaint()
        t = dt.datetime(self.start_day.date().year(), self.start_day.date().month(), self.start_day.date().day(), 0, 0, 0)
        end_day_ = dt.datetime(self.end_day.date().year(), self.end_day.date().month(), self.end_day.date().day(), 0, 0, 0)
        test_money = self.worker.test_(self.now_coin, t, end_day_)
        self.worker.start()
        self._yield.setText('수익률 : '+str(round((test_money-1)*100,2))+'%')
    def get_my_krw(self):
        # 보유중인 원화
        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
        }

        jwt_token = jwt.encode(payload, secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.get("https://api.upbit.com/v1/accounts", headers=headers)
        for i in res.json():
            if i['currency'] == "KRW":
                    return str(int(int(i['balance'].split('.')[0])*0.9995)-1)

    def ratio(self, per):
        money = int(self.label_115.text()[:-3])*per//100
        self.edit_search_1.setText(str(money))
    def auto_trading(self):
        # print(self.edit_search_1.text().isdigit())
        if self.edit_search_1.text().isdigit() and int(self.edit_search_1.text()) > 5000:
            self.worker.resume(self.now_coin, int(self.edit_search_1.text()))
            self.worker.start()
            self.auto_trading_alarm.show()
    def stop_trading(self):
        self.worker.pause()
        self.auto_trading_alarm.hide()
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setInputMethodHints(PyQt5.QtCore.Qt.ImhNone)
        self.centralwidget = PyQt5.QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: rgb(255,255,255)")
        self.now_coin = 'BTC'
        self.chk_auto = 1
        self.worker = Worker()
        # 검색창
        self.edit_search = PyQt5.QtWidgets.QLineEdit(self.centralwidget)
        self.edit_search.setGeometry(PyQt5.QtCore.QRect(238, 90, 400, 49))
        font = PyQt5.QtGui.QFont()
        font.setPointSize(20)
        self.edit_search.setFont(font)
        self.edit_search.setObjectName("edit_search")
        # 자동완성 리스트
        url = "https://api.upbit.com/v1/market/all?isDetails=false"

        headers = {"Accept": "application/json"}

        response = requests.get(url, headers=headers)
        response = response.json()
        self.coin_list = []
        for i in response:
            if i['market'][:3] == 'KRW':
                self.coin_list.append(i['korean_name'] + '/' + i['market'][4:])

        # Completer 생성 및 QCombo 연결
        completer = QCompleter(self.coin_list)
        # 포함된 항목 모두 검색
        completer.setFilterMode(Qt.MatchContains)
        # 대소문자
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        # 검색창에 자동완성 연결
        self.edit_search.setCompleter(completer)
        self.edit_search.returnPressed.connect(self.coin_change)
        # 검색창 돋보기 이미지
        self.image_search = PyQt5.QtWidgets.QGraphicsView(self.centralwidget)
        self.image_search.setGeometry(PyQt5.QtCore.QRect(175, 90, 49, 49))
        self.image_search.setStyleSheet("border-image: url(resources/search.png); background-repeat: no-repeat;")
        self.image_search.setObjectName("image_search")

        # 왼쪽 프레임
        self.frame = PyQt5.QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(PyQt5.QtCore.QRect(0, 112, 1534, 1435))
        self.frame.setFrameShape(PyQt5.QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(PyQt5.QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.setStyleSheet("background-color:none;")

        #차트
        self.webEngineView = PyQt5.QtWebEngineWidgets.QWebEngineView(self.frame)
        self.webEngineView.setGeometry(PyQt5.QtCore.QRect(143, 70, 1391, 857))
        self.webEngineView.setUrl(PyQt5.QtCore.QUrl("https://upbit.com/full_chart?code=CRIX.UPBIT.KRW-BTC"))

        # 과거 데이터 테스트 텍스트
        self.back_trading = PyQt5.QtWidgets.QLabel(self.centralwidget)
        self.back_trading.setGeometry(PyQt5.QtCore.QRect(710, 25, 281, 70))
        self.back_trading.setObjectName("back_trading")
        font = PyQt5.QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.back_trading.setFont(font)

        # 과거 데이터 전략 선택
        self.comboBox = PyQt5.QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(PyQt5.QtCore.QRect(700, 90, 182, 49))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("  변동성 돌파 전략")
        self.comboBox.addItem("  전략 준비중")
        self.comboBox.addItem("  전략 준비중")
        font = PyQt5.QtGui.QFont()
        font.setPointSize(12)
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet("border: 1px solid blue; background-color:white; color: black;")

        #시작하는 날 선택
        self.start_day = QtWidgets.QDateEdit(self.centralwidget)
        self.start_day.setGeometry(QtCore.QRect(920, 90, 150, 49))
        self.start_day.setDateTime(QtCore.QDateTime(QtCore.QDate(2022, 3, 20), QtCore.QTime(0, 0, 0)))
        self.start_day.setObjectName("dateEdit")
        # 끝나는 날 선택
        self.end_day = QtWidgets.QDateEdit(self.centralwidget)
        self.end_day.setGeometry(QtCore.QRect(1085, 90, 150, 49))
        self.end_day.setDateTime(QtCore.QDateTime(QtCore.QDate(2022, 3, 25), QtCore.QTime(0, 0, 0)))
        self.end_day.setObjectName("dateEdit")
        # 테스트 버튼
        self.pushButton_4 = PyQt5.QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(PyQt5.QtCore.QRect(1250, 90, 98, 49))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setStyleSheet("border: 1px solid blue; background-color:white; color: blue;")
        self.pushButton_4.clicked.connect(self.test_button)

        # 수익률
        self._yield = PyQt5.QtWidgets.QLabel(self.centralwidget)
        self._yield.setGeometry(PyQt5.QtCore.QRect(1370, 90, 281, 70))
        self._yield.setObjectName("_yield")
        font = PyQt5.QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self._yield.setFont(font)
        self._yield.hide()

        # 오른쪽 프레임
        self.frame_2 = PyQt5.QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setStyleSheet("background-color:none;")
        self.frame_2.setGeometry(PyQt5.QtCore.QRect(1534, 0, 960, 1079))
        self.frame_2.setFrameShape(PyQt5.QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(PyQt5.QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")


        # 보유종목
        self.comboBox1 = PyQt5.QtWidgets.QComboBox(self.frame_2)
        self.comboBox1.setGeometry(PyQt5.QtCore.QRect(30, 90, 182, 49))
        self.comboBox1.setObjectName("comboBox1")
        self.comboBox1.addItem("보유종목")
        self.comboBox1.addItem("doge")
        self.comboBox1.addItem("btc")
        font = PyQt5.QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.comboBox1.setFont(font)
        self.comboBox1.setStyleSheet("border: 1px solid blue; background-color:white; color: black;")

        # 주문가능
        self.label_114 = PyQt5.QtWidgets.QLabel(self.frame_2)
        self.label_114.setGeometry(PyQt5.QtCore.QRect(20, 170, 281, 70))
        self.label_114.setObjectName("label_114")
        font = PyQt5.QtGui.QFont()
        font.setPointSize(8)
        self.label_114.setFont(font)

        # 주문금액
        self.label_115 = PyQt5.QtWidgets.QLineEdit(self.frame_2)
        self.label_115.setGeometry(PyQt5.QtCore.QRect(120, 190, 240, 40))
        self.label_115.setObjectName("label_115")
        font = PyQt5.QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_115.setFont(font)
        self.label_115.setText(str(self.get_my_krw())+'KRW')
        # 10%
        self.pushButton_5 = PyQt5.QtWidgets.QPushButton(self.frame_2)
        self.pushButton_5.setGeometry(PyQt5.QtCore.QRect(20, 240, 56, 30))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setStyleSheet("border: 1px solid grey; background-color:white; color: black;")
        self.pushButton_5.clicked.connect(lambda: self.ratio(10))
        # 20%
        self.pushButton_6 = PyQt5.QtWidgets.QPushButton(self.frame_2)
        self.pushButton_6.setGeometry(PyQt5.QtCore.QRect(85, 240, 56, 30))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.setStyleSheet("border: 1px solid grey; background-color:white; color: black;")
        self.pushButton_6.clicked.connect(lambda: self.ratio(20))
        # 50%
        self.pushButton_7 = PyQt5.QtWidgets.QPushButton(self.frame_2)
        self.pushButton_7.setGeometry(PyQt5.QtCore.QRect(150, 240, 56, 30))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.setStyleSheet("border: 1px solid grey; background-color:white; color: black;")
        self.pushButton_7.clicked.connect(lambda: self.ratio(50))
        # 100%
        self.pushButton_8 = PyQt5.QtWidgets.QPushButton(self.frame_2)
        self.pushButton_8.setGeometry(PyQt5.QtCore.QRect(215, 240, 56, 30))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.setStyleSheet("border: 1px solid grey; background-color:white; color: black;")
        self.pushButton_8.clicked.connect(lambda: self.ratio(100))
        # 직접입력
        self.pushButton_9 = PyQt5.QtWidgets.QPushButton(self.frame_2)
        self.pushButton_9.setGeometry(PyQt5.QtCore.QRect(280, 240, 84, 30))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_9.setStyleSheet("border: 1px solid grey; background-color:white; color: black;")

        # 주문총액
        self.label_116 = PyQt5.QtWidgets.QLabel(self.frame_2)
        self.label_116.setGeometry(PyQt5.QtCore.QRect(20, 280, 281, 70))
        self.label_116.setObjectName("label_116")
        font = PyQt5.QtGui.QFont()
        font.setPointSize(8)
        self.label_116.setFont(font)

        # 주문 금액
        self.edit_search_1 = PyQt5.QtWidgets.QLineEdit(self.frame_2)
        self.edit_search_1.setGeometry(PyQt5.QtCore.QRect(120, 295, 240, 40))
        font = PyQt5.QtGui.QFont()
        font.setPointSize(20)
        self.edit_search_1.setFont(font)
        self.edit_search_1.setValidator(QIntValidator())
        self.edit_search_1.setObjectName("edit_search_1")

        #자동 매매 시작
        self.pushButton_10 = PyQt5.QtWidgets.QPushButton(self.frame_2)
        self.pushButton_10.setGeometry(PyQt5.QtCore.QRect(20, 360, 160, 40))
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_10.setStyleSheet("border: 1px solid grey; background-color:red; color: white;")
        self.pushButton_10.clicked.connect(self.auto_trading)
        # 자동 매매 종료
        self.pushButton_11 = PyQt5.QtWidgets.QPushButton(self.frame_2)
        self.pushButton_11.setGeometry(PyQt5.QtCore.QRect(210, 360, 160, 40))
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_11.setStyleSheet("border: 1px solid grey; background-color:blue; color: white;")
        self.pushButton_11.clicked.connect(self.stop_trading)

        self.auto_trading_alarm = PyQt5.QtWidgets.QLabel(self.frame_2)
        self.auto_trading_alarm.setGeometry(PyQt5.QtCore.QRect(80, 400, 281, 25))
        self.auto_trading_alarm.setText('자동매매 실행중!')
        self.auto_trading_alarm.setObjectName("auto_trading_alarm")
        font = PyQt5.QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.auto_trading_alarm.setFont(font)
        self.auto_trading_alarm.setStyleSheet("color: red;")
        self.auto_trading_alarm.hide()

        # 자동 매매 거래 내역
        self.label_117 = PyQt5.QtWidgets.QLabel(self.frame_2)
        self.label_117.setGeometry(PyQt5.QtCore.QRect(7, 430, 281, 70))
        self.label_117.setObjectName("label_117")
        font = PyQt5.QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_117.setFont(font)

        # 자동매매 거래 내역 리스트
        self.table_currentCoinList = PyQt5.QtWidgets.QTableWidget(self.frame_2)
        self.table_currentCoinList.setGeometry(PyQt5.QtCore.QRect(0, 485, 376, 560))
        sizePolicy = PyQt5.QtWidgets.QSizePolicy(PyQt5.QtWidgets.QSizePolicy.Fixed, PyQt5.QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_currentCoinList.sizePolicy().hasHeightForWidth())
        self.table_currentCoinList.setSizePolicy(sizePolicy)
        self.table_currentCoinList.setMouseTracking(False)
        self.table_currentCoinList.setStyleSheet(
            """
            QHeaderView::section {
                background-color:#404040;
                color:#FFFFFF;
            }
            """
        )
        self.table_currentCoinList.setHorizontalScrollBarPolicy(PyQt5.QtCore.Qt.ScrollBarAlwaysOff)
        self.table_currentCoinList.setSizeAdjustPolicy(PyQt5.QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.table_currentCoinList.setAutoScrollMargin(16)
        self.table_currentCoinList.setDefaultDropAction(PyQt5.QtCore.Qt.IgnoreAction)
        self.table_currentCoinList.setAlternatingRowColors(True)
        self.table_currentCoinList.setSelectionBehavior(PyQt5.QtWidgets.QAbstractItemView.SelectRows)
        self.table_currentCoinList.setRowCount(30)
        self.table_currentCoinList.setColumnCount(5)
        self.table_currentCoinList.setObjectName("table_currentCoinList")
        item = PyQt5.QtWidgets.QTableWidgetItem()
        self.table_currentCoinList.setHorizontalHeaderItem(0, item)
        item = PyQt5.QtWidgets.QTableWidgetItem()
        self.table_currentCoinList.setHorizontalHeaderItem(1, item)
        item = PyQt5.QtWidgets.QTableWidgetItem()
        self.table_currentCoinList.setHorizontalHeaderItem(2, item)
        item = PyQt5.QtWidgets.QTableWidgetItem()
        self.table_currentCoinList.setHorizontalHeaderItem(3, item)
        item = PyQt5.QtWidgets.QTableWidgetItem()
        self.table_currentCoinList.setHorizontalHeaderItem(4, item)

        self.table_currentCoinList.horizontalHeader().setVisible(True)
        self.table_currentCoinList.horizontalHeader().setFixedHeight(45)
        self.table_currentCoinList.horizontalHeader().setDefaultSectionSize(70)  # 테이블 기본 열 크기
        self.table_currentCoinList.horizontalHeader().setSortIndicatorShown(True)
        self.table_currentCoinList.horizontalHeader().setStretchLastSection(False)
        self.table_currentCoinList.verticalHeader().setVisible(False)  # 행 번호 안보이게 설정
        self.table_currentCoinList.verticalHeader().setCascadingSectionResizes(False)
        self.table_currentCoinList.verticalHeader().setDefaultSectionSize(35)  # 테이블 기본 행 크기
        self.table_currentCoinList.verticalHeader().setHighlightSections(True)

        # 왼쪽 메뉴 프레임
        self.frame = PyQt5.QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(PyQt5.QtCore.QRect(0, 0, 140, 1079))
        self.frame.setStyleSheet("background-color: rgb(50, 90, 160)")  # 배경색 설정
        self.frame.setFrameShape(PyQt5.QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(PyQt5.QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # 메뉴-마이페이지 버튼
        self.menuButton_myPage_3 = PyQt5.QtWidgets.QPushButton(self.frame)
        self.menuButton_myPage_3.setGeometry(PyQt5.QtCore.QRect(29, 70, 84, 84))
        self.menuButton_myPage_3.setObjectName("menuButton_myPage_3")
        self.menuButton_myPage_3.setStyleSheet(
            """
            QPushButton {
                border-image: url(resources/menu_myPage.png);
                background-repeat: no-repeat;
            }
            QPushButton:pressed {
                border-image: url(resources/menu_myPage_clicked.png);
                background-repeat: no-repeat;
            }
            """
        )

        # 메뉴-트레이딩 버튼
        self.menuButton_trading_3 = PyQt5.QtWidgets.QPushButton(self.frame)
        self.menuButton_trading_3.setGeometry(PyQt5.QtCore.QRect(29, 210, 84, 84))
        self.menuButton_trading_3.setObjectName("menuButton_trading_3")
        self.menuButton_trading_3.setStyleSheet(
            """
            QPushButton {
                border-image: url(resources/menu_trading.png);
                background-repeat: no-repeat;
            }
            QPushButton:pressed {
                border-image: url(resources/menu_trading_clicked.png);
                background-repeat: no-repeat;
            }
            """
        )

        # 메뉴-거래(사고팔기) 버튼
        self.menuButton_chart_3 = PyQt5.QtWidgets.QPushButton(self.frame)
        self.menuButton_chart_3.setGeometry(PyQt5.QtCore.QRect(29, 351, 84, 84))
        self.menuButton_chart_3.setObjectName("menuButton_chart_3")
        self.menuButton_chart_3.setStyleSheet(
            """
            QPushButton {
                border-image: url(resources/menu_chart.png);
                background-repeat: no-repeat;
            }
            QPushButton:pressed {
                border-image: url(resources/menu_chart_clicked.png);
                background-repeat: no-repeat;
            }
            """
        )

        # 메뉴-자동거래 버튼
        self.menuButton_autoTrading_3 = PyQt5.QtWidgets.QPushButton(self.frame)
        self.menuButton_autoTrading_3.setGeometry(PyQt5.QtCore.QRect(29, 491, 84, 84))
        self.menuButton_autoTrading_3.setObjectName("menuButton_autoTrading_3")
        self.menuButton_autoTrading_3.setStyleSheet(
            """
            QPushButton {
                border-image: url(resources/menu_autoTrading.png);
                background-repeat: no-repeat;
            }
            QPushButton:pressed {
                border-image: url(resources/menu_autoTrading_clicked.png);
                background-repeat: no-repeat;
            }
            """
        )

        # 메뉴-환경설정 버튼
        self.menuButton_setting_3 = PyQt5.QtWidgets.QPushButton(self.frame)
        self.menuButton_setting_3.setGeometry(PyQt5.QtCore.QRect(29, 632, 84, 84))
        self.menuButton_setting_3.setObjectName("menuButton_setting_3")
        self.menuButton_setting_3.setStyleSheet(
            """
            QPushButton {
                border-image: url(resources/menu_setting.png);
                background-repeat: no-repeat;
            }
            QPushButton:pressed {
                border-image: url(resources/menu_setting_clicked.png);
                background-repeat: no-repeat;
            }
            """
        )

        # 메뉴-종료 버튼
        self.menuButton_exit_3 = PyQt5.QtWidgets.QPushButton(self.frame)
        self.menuButton_exit_3.setGeometry(PyQt5.QtCore.QRect(29, 913, 84, 84))
        self.menuButton_exit_3.setObjectName("menuButton_exit_3")
        self.menuButton_exit_3.setStyleSheet(
            """
            QPushButton {
                border-image: url(resources/menu_exit.png);
                background-repeat: no-repeat;
            }
            QPushButton:pressed {
                border-image: url(resources/menu_exit_clicked.png);
                background-repeat: no-repeat;
            }
            """
        )

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        PyQt5.QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = PyQt5.QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_4.setText(_translate("MainWindow", "테스트"))
        self.pushButton_5.setText(_translate("MainWindow", "10%"))
        self.pushButton_6.setText(_translate("MainWindow", "20%"))
        self.pushButton_7.setText(_translate("MainWindow", "50%"))
        self.pushButton_8.setText(_translate("MainWindow", "100%"))
        self.pushButton_9.setText(_translate("MainWindow", "직접입력"))
        self.pushButton_10.setText(_translate("MainWindow", "자동매매"))
        self.pushButton_11.setText(_translate("MainWindow", "종료하기"))
        self.label_114.setText(_translate("MainWindow", "주문가능"))
        self.label_116.setText(_translate("MainWindow", "주문총액(KRW)"))
        self.label_117.setText(_translate("MainWindow", "자동 매매 거래 내역"))
        self.back_trading.setText(_translate("MainWindow", "과거 데이터 테스트"))
if __name__ == "__main__":
    import sys
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    MainWindow = PyQt5.QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
