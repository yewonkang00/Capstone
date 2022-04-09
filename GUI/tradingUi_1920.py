import time

from PyQt5 import QtCore, QtGui, QtWidgets
import os
import jwt
import uuid
import requests
import hashlib
from urllib.parse import urlencode
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
access_key = ''
secret_key = ''
user_email = ''

class Ui_MainWindow(QtWidgets.QWidget):
    def trade(self):
        if self.safty:
            if self.isEmpty():
                QMessageBox.about(self, 'error!', '입력을 확인하세요!')
            else :
                if self.limit_market == 0 and self.Totalorder.text() == '':
                    self.ratio(-1)
                server_url = "https://api.upbit.com/v1/orders"
                if self.buy_sell == 0 and self.limit_market == 0:  # 지정가 주문
                    #price : 코인 개당 가격
                    query = {
                        'market': 'KRW-'+self.now_coin,
                        'side': ['bid', 'ask'][self.buy_sell],
                        'volume': float(self.order_quantity.text()),
                        'price': int(int(self.Totalorder.text())/float(self.order_quantity.text())),
                        'ord_type': 'limit',
                    }
                elif self.limit_market == 0:
                    query = {
                        'market': 'KRW-' + self.now_coin,
                        'side': ['bid', 'ask'][self.buy_sell],
                        'volume': float(self.order_quantity.text()),
                        'price': int(self.buy_price.text()),
                        'ord_type': 'limit',
                    }
                elif self.buy_sell == 0:  # 시장가 매수
                    query = {
                        'market': 'KRW-'+self.now_coin,
                        'side': 'bid',
                        'price': int(self.order_quantity.text()),
                        'ord_type': 'price',
                    }
                else:  # 시장가 매도
                    query = {
                        'market': 'KRW-'+self.now_coin,
                        'side': 'ask',
                        'volume': float(self.order_quantity.text()),
                        'ord_type': 'market',
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

                res = requests.post(server_url, params=query, headers=headers)
                res = res.json()
                if 'uuid' in res:#거래 성공
                    QMessageBox.about(self, 'success!', '거래를 성공했습니다!')
                else :
                    QMessageBox.about(self, 'error!', res['error']['message'])

        self.reset()
    def trade_list(self):
        if self.buy_sell < 2 or self.buy_sell % 2 == 1:
            self.pushButton_3.setText('미체결')
            self.pushButton_3.setStyleSheet("Color : white;background-color:#6756BE;")
            self.buy_sell = 2
        else :
            self.pushButton_3.setText('거래내역')
            self.pushButton_3.setStyleSheet("Color : white;background-color:#369F36;")
            self.buy_sell += 1

        self.buy_price.hide()
        self.buy_minus.hide()
        self.buy_plus.hide()
        self.Totalorder.hide()
        self.label_44.hide()
        self.label_46.hide()
        self.label_45.hide()
        self.order_quantity.hide()
        self.order_ratio10.hide()
        self.order_ratio25.hide()
        self.order_ratio50.hide()
        self.order_ratio100.hide()
        self.order_ratio_self.hide()

        self.pushButton_4.hide()
        self.pushButton_5.hide()
        self.label_42.hide()
        self.can_money.hide()
        self.label_43.hide()
        self.pushButton_6.hide()
        self.pushButton_7.hide()

        self.pushButton.setStyleSheet("default;")
        self.pushButton_2.setStyleSheet("default;")

    def reset(self):
        # 색칠
        self.pushButton_3.setStyleSheet("default;")
        self.pushButton_3.setText('거래내역')
        if self.buy_sell == 0:
            self.pushButton_2.setStyleSheet("default;")
            self.pushButton.setStyleSheet("Color : white;background-color:#FF5733;")
            self.pushButton_7.setStyleSheet("Color : white;background-color:#FF5733;")
        elif self.buy_sell == 1:
            self.pushButton.setStyleSheet("default;")
            self.pushButton_2.setStyleSheet("Color : white;background-color:#54A0FF;")
            self.pushButton_7.setStyleSheet("Color : white;background-color:#54A0FF;")
        if self.limit_market == 0:
            self.pushButton_5.setStyleSheet("default;")
            self.pushButton_4.setStyleSheet("Color : white;background-color:#FF5733;")
        elif self.limit_market == 1:
            self.pushButton_4.setStyleSheet("default;")
            self.pushButton_5.setStyleSheet("Color : white;background-color:#FF5733;")

        if self.buy_sell == 0:
            self.can_money.setText(self.my_money('KRW'))
        else:
            self.can_money.setText(self.my_money(self.now_coin))
        if self.can_money.text() == '':
            self.can_money.setText('0')
        self.buy_price.setText(str(self.now_price('KRW-'+self.now_coin)))
        self.order_quantity.setText('')
        self.Totalorder.setText('')
    def ratio(self, per):
        if self.buy_sell == 0 and self.limit_market == 0:
            # 지정가 매수
            if per > 0:
                self.Totalorder.setText(str(int(self.can_money.text()) * per // 100))
                self.order_quantity.setText(str(int(self.can_money.text()) * per // 100 / int(self.buy_price.text())))
            elif self.isEmpty():
                QMessageBox.about(self, 'error!', '입력을 확인하세요!')
            else:
                self.Totalorder.setText(str(int(float(self.order_quantity.text())*int(self.buy_price.text()))))
        if self.buy_sell == 0 and self.limit_market == 1:
            #시장가 매수
            if per > 0:
                self.order_quantity.setText(str(int(self.can_money.text())*per//100))
        if self.buy_sell == 1 and self.limit_market == 0:
            #지정가 매도
            if per > 0:
                self.order_quantity.setText(str(float(self.can_money.text())*per/100))
                self.Totalorder.setText(str(int(float(self.can_money.text())*per/100*int(self.buy_price.text()))))
            elif self.isEmpty():
                QMessageBox.about(self, 'error!', '입력을 확인하세요!')
            else:
                self.Totalorder.setText(str(int(float(self.order_quantity.text())*int(self.buy_price.text()))))
        if self.buy_sell == 1 and self.limit_market == 1:
            #시장가 매도
            if per > 0:
                self.order_quantity.setText(str(float(self.can_money.text())*per/100))

    def isEmpty(self):
        if self.limit_market == 0:
            return 1 if (self.buy_price.text() == '' or self.order_quantity.text() == '') else 0
        else :
            return 1 if self.order_quantity.text() == '' else 0
    def change(self):
        if self.buy_sell == 0:
            self.label_43.setText("KRW")
            self.label_44.setText("매수가격(KRW)")
            self.label_45.setText("주문수량("+self.now_coin+")")
            self.label_46.setText("주문총액(KRW)")
            self.pushButton_7.setText("매수")
        elif self.buy_sell == 1:
            self.label_43.setText(self.now_coin)
            self.label_44.setText("매도가격(KRW)")
            self.label_45.setText("주문수량("+self.now_coin+")")
            self.label_46.setText("주문총액(KRW)")
            self.pushButton_7.setText("매도")
        if self.limit_market == 0:
            self.buy_price.show()
            self.buy_minus.show()
            self.buy_plus.show()
            self.Totalorder.show()
            self.label_44.show()
            self.label_46.show()

            self.label_44.show()
            self.label_46.show()
            self.label_45.show()
            self.order_quantity.show()
            self.order_ratio10.show()
            self.order_ratio25.show()
            self.order_ratio50.show()
            self.order_ratio100.show()
            self.order_ratio_self.show()

            self.pushButton_4.show()
            self.pushButton_5.show()
            self.label_42.show()
            self.can_money.show()
            self.label_43.show()
            self.pushButton_6.show()
            self.pushButton_7.show()

            self.label_46.move(106, 860)
            self.order_quantity.move(300, 740)
            self.order_ratio10.move(300, 797)
            self.order_ratio25.move(401, 797)
            self.order_ratio50.move(502, 797)
            self.order_ratio100.move(603, 797)
            self.order_ratio_self.move(704, 797)
        elif self.limit_market == 1:
            self.buy_price.hide()
            self.buy_minus.hide()
            self.buy_plus.hide()
            self.Totalorder.hide()
            self.label_44.hide()
            self.label_45.hide()
            self.label_46.move(106, 680)
            self.order_quantity.move(300, 670)
            self.order_ratio10.move(300, 727)
            self.order_ratio25.move(401, 727)
            self.order_ratio50.move(502, 727)
            self.order_ratio100.move(603, 727)
            self.order_ratio_self.move(704, 727)
        self.reset()
    def About_event(self):
        QMessageBox.about(self, 'About Title', 'About Message')
    def btn_plus(self):
        if self.buy_price.text() == '':
            self.buy_price.setText('0')
        else:
            self.buy_price.setText(str(int(self.buy_price.text())+self.pnm_value))
    def btn_minus(self):
        if self.buy_price.text() == '' or int(self.buy_price.text()) < self.pnm_value:
            self.buy_price.setText('0')
        else:
            self.buy_price.setText(str(int(self.buy_price.text())-self.pnm_value))
    def buy_sell_click(self, code):
        if code != self.buy_sell:
            self.buy_sell = code
            self.limit_market = 0
            self.change()
    def limit_market_click(self, code):
        if code != self.limit_market:
            self.limit_market = code
            self.change()
    def my_money(self, coin_name):
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
            if i['currency'] == coin_name:
                if coin_name == "KRW":
                    return str(int(int(i['balance'].split('.')[0])*0.9995)-1)
                else :
                    return i['balance']
    def now_price(self, coin_name):
        url = "https://api.upbit.com/v1/candles/minutes/60"
        querystring = {"market": coin_name, "count": 1}
        response = requests.request("GET", url, params=querystring)
        response = response.json()
        return int(response[0]['trade_price'])
    def __init__(self):
        super().__init__()
        self.safty = 1
        self.buy_sell = 0  # 0 : 매수, 1 : 매도 2> : 거래 리스트
        self.limit_market = 0  # 0 : 지정가, 1 : 시장가

        self.now_coin = 'SAND'
        self.pnm_value = 1000
        self.setWindowTitle("HY-coin")
        self.setFixedSize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: rgb(255,255,255)")

        # 검색창
        self.edit_search = QtWidgets.QLineEdit(self.centralwidget)
        self.edit_search.setGeometry(QtCore.QRect(267, 56, 632, 49))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.edit_search.setFont(font)
        self.edit_search.setObjectName("edit_search")

        # 검색창 돋보기 이미지
        self.image_search = QtWidgets.QGraphicsView(self.centralwidget)
        self.image_search.setGeometry(QtCore.QRect(204, 56, 49, 49))
        self.image_search.setStyleSheet("border-image: url(resources/search.png); background-repeat: no-repeat;")
        self.image_search.setObjectName("image_search")


        # 왼쪽 프레임
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 112, 1379, 1435))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.setStyleSheet("background-color:none;")

        # 코인이미지
        self.image_coin = QtWidgets.QGraphicsView(self.frame)
        self.image_coin.setGeometry(QtCore.QRect(211, 24, 49, 49))
        self.image_coin.setStyleSheet("border-image: url(resources/bitcoin.png); background-repeat: no-repeat;")
        self.image_coin.setObjectName("image_coin")

        # 코인명(예.비트코인)
        self.label_coinName = QtWidgets.QLabel(self.frame)
        self.label_coinName.setGeometry(QtCore.QRect(267, 14, 281, 70))
        self.label_coinName.setObjectName("label_coinName")
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.label_coinName.setFont(font)

        # 코인명 옆에 회색으로 알파벳 코드(예.BTC)
        self.label_coinNickname = QtWidgets.QLabel(self.frame)
        self.label_coinNickname.setGeometry(QtCore.QRect(372, 4, 211, 98))
        self.label_coinNickname.setObjectName("label_coinNickname")
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_coinNickname.setFont(font)
        self.label_coinNickname.setStyleSheet("color: GREY;")

        # 호가 레이블
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(267, 56, 211, 98))
        self.label_3.setObjectName("label_3")
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.label_3.setFont(font)

        # 호가 테이블
        self.tableWidget = QtWidgets.QTableWidget(self.frame)
        self.tableWidget.setGeometry(QtCore.QRect(267, 141, 632, 740))
        self.tableWidget.setRowCount(20)  # 테이블 기본 행 갯수
        self.tableWidget.setColumnCount(7)  # 테이블 기본 열 갯수
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setVisible(False)  # 수직헤더
        self.tableWidget.horizontalHeader().setVisible(False)  # 수평헤더
        self.tableWidget.horizontalHeader().setDefaultSectionSize(90)  # 테이블 기본 열 크기
        self.tableWidget.verticalHeader().setDefaultSectionSize(35)  # 테이블 기본 행 크기

        # 테이블 헤더: 일괄취소(파란색)
        self.button_cancel_1 = QtWidgets.QPushButton(self.frame)
        self.button_cancel_1.setGeometry(QtCore.QRect(267, 842, 127, 49))
        self.button_cancel_1.setObjectName("button_cancel_1")
        self.button_cancel_1.setStyleSheet("border: 1px solid grey; background-color:white; color: blue;")

        # 오른쪽 프레임
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setStyleSheet("background-color:none;")
        self.frame_2.setGeometry(QtCore.QRect(984, 0, 960, 1079))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        # 매수버튼
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setGeometry(QtCore.QRect(84, 450, 246, 84))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("매수")
        self.pushButton.clicked.connect(lambda: self.buy_sell_click(0))

        # 매도버튼
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_2.setGeometry(QtCore.QRect(323, 450, 246, 84))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("매도")
        self.pushButton_2.clicked.connect(lambda: self.buy_sell_click(1))

        # 거래내역
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_3.setGeometry(QtCore.QRect(562, 450, 246, 84))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText("거래내역")
        self.pushButton_3.clicked.connect(self.trade_list)

        # 지정가버튼
        self.pushButton_4 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_4.setGeometry(QtCore.QRect(103, 536, 154, 54))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setText("지정가")
        self.pushButton_4.clicked.connect(lambda: self.limit_market_click(0))

        # 시정가버튼
        self.pushButton_5 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_5.setGeometry(QtCore.QRect(270, 536, 154, 54))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setText("시장가")
        self.pushButton_5.clicked.connect(lambda: self.limit_market_click(1))

        # 하단 초기화버튼
        self.pushButton_6 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_6.setGeometry(QtCore.QRect(103, 936, 323, 74))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.setText("초기화")
        self.pushButton_6.clicked.connect(self.reset)

        # 하단 매수버튼
        self.pushButton_7 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_7.setGeometry(QtCore.QRect(465, 936, 323, 74))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(self.trade)
        self.pushButton_7.setText("매수")

        # 주문가능 텍스트
        self.label_42 = QtWidgets.QLabel(self.frame_2)
        self.label_42.setGeometry(QtCore.QRect(106, 610, 141, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_42.setFont(font)
        self.label_42.setObjectName("label_42")
        self.label_42.setText("주문가능")

        #주문가능 가격
        self.can_money = QtWidgets.QLineEdit(self.frame_2)
        self.can_money.setGeometry(QtCore.QRect(300, 610, 410, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.can_money.setFont(font)
        self.can_money.setReadOnly(True)
        self.can_money.setObjectName("can_money")

        # 주문가능 단위
        self.label_43 = QtWidgets.QLabel(self.frame_2)
        self.label_43.setGeometry(QtCore.QRect(726, 610, 141, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_43.setFont(font)
        self.label_43.setObjectName("label_43")
        self.label_43.setText("KRW")

        # 매수가격(KRW)
        self.label_44 = QtWidgets.QLabel(self.frame_2)
        self.label_44.setGeometry(QtCore.QRect(106, 680, 141, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_44.setFont(font)
        self.label_44.setObjectName("label_44")
        self.label_44.setText("매수가격(KRW)")

        # 매수가격 입력창
        self.buy_price = QtWidgets.QLineEdit(self.frame_2)
        self.buy_price.setGeometry(QtCore.QRect(300, 670, 410, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.buy_price.setFont(font)
        self.buy_price.setValidator(QIntValidator())
        self.buy_price.setObjectName("buy_price")

        # 매수가격 플러스버튼
        self.buy_plus = QtWidgets.QPushButton(self.frame_2)
        self.buy_plus.setGeometry(QtCore.QRect(760, 670, 50, 50))
        self.buy_plus.setObjectName("buy_plus")
        self.buy_plus.setText("+")
        self.buy_plus.clicked.connect(self.btn_plus)

        # 매수가격 마이너스버튼
        self.buy_minus = QtWidgets.QPushButton(self.frame_2)
        self.buy_minus.setGeometry(QtCore.QRect(710, 670, 50, 50))
        self.buy_minus.setObjectName("buy_minus")
        self.buy_minus.setText("-")
        self.buy_minus.clicked.connect(self.btn_minus)
        # 주문수량(BTC)
        self.label_45 = QtWidgets.QLabel(self.frame_2)
        self.label_45.setGeometry(QtCore.QRect(106, 750, 141, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_45.setFont(font)
        self.label_45.setObjectName("label_45")
        self.label_45.setText("주문수량("+self.now_coin+")")


        # 주문수량 입력창
        self.order_quantity = QtWidgets.QLineEdit(self.frame_2)
        self.order_quantity.setGeometry(QtCore.QRect(300, 740, 500, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.order_quantity.setFont(font)
        self.order_quantity.setValidator(QDoubleValidator(0.99,99.99,10))
        self.order_quantity.setObjectName("order_quantity")

        # 10% 버튼
        self.order_ratio10 = QtWidgets.QPushButton(self.frame_2)
        self.order_ratio10.setGeometry(QtCore.QRect(300, 797, 95, 40))
        self.order_ratio10.setObjectName("order_ratio10")
        self.order_ratio10.clicked.connect(lambda : self.ratio(10))
        self.order_ratio10.setText("10%")

        # 25% 버튼
        self.order_ratio25 = QtWidgets.QPushButton(self.frame_2)
        self.order_ratio25.setGeometry(QtCore.QRect(401, 797, 95, 40))
        self.order_ratio25.setObjectName("order_ratio25")
        self.order_ratio25.clicked.connect(lambda: self.ratio(25))
        self.order_ratio25.setText("25%")

        # 50% 버튼
        self.order_ratio50 = QtWidgets.QPushButton(self.frame_2)
        self.order_ratio50.setGeometry(QtCore.QRect(502, 797, 95, 40))
        self.order_ratio50.setObjectName("order_ratio50")
        self.order_ratio50.clicked.connect(lambda: self.ratio(50))
        self.order_ratio50.setText("50%")

        # 100% 버튼
        self.order_ratio100 = QtWidgets.QPushButton(self.frame_2)
        self.order_ratio100.setGeometry(QtCore.QRect(603, 797, 95, 40))
        self.order_ratio100.setObjectName("order_ratio100")
        self.order_ratio100.clicked.connect(lambda: self.ratio(100))
        self.order_ratio100.setText("100%")

        # 직접입력 버튼
        self.order_ratio_self = QtWidgets.QPushButton(self.frame_2)
        self.order_ratio_self.setGeometry(QtCore.QRect(704, 797, 95, 40))
        self.order_ratio_self.setObjectName("order_ratio_self")
        self.order_ratio_self.clicked.connect(lambda: self.ratio(-1))
        self.order_ratio_self.setText("직접입력")

        # 주문총액(KRW)
        self.label_46 = QtWidgets.QLabel(self.frame_2)
        self.label_46.setGeometry(QtCore.QRect(106, 860, 141, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_46.setFont(font)
        self.label_46.setObjectName("label_46")
        self.label_46.setText("주문총액(KRW)")

        # 주문총액 입력창
        self.Totalorder = QtWidgets.QLineEdit(self.frame_2)
        self.Totalorder.setGeometry(QtCore.QRect(300, 850, 500, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Totalorder.setFont(font)
        self.Totalorder.setReadOnly(True)
        self.Totalorder.setObjectName("Totalorder")

        # 종목정보 Frame
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setStyleSheet("background-color:none;")
        self.frame_3.setGeometry(QtCore.QRect(984+28, 98, 1323, 350))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")

        #거래량
        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setGeometry(QtCore.QRect(56, 56, 141, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # 거래량 Number
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        self.label_4.setGeometry(QtCore.QRect(98, 56, 211, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        # 보유종목
        self.comboBox = QtWidgets.QComboBox(self.frame_3)
        self.comboBox.setGeometry(QtCore.QRect(56, 0, 281, 49))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("보유종목")
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.comboBox.setFont(font)

        # 거래량
        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setGeometry(QtCore.QRect(56, 56, 141, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # 거래량 Number
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        self.label_4.setGeometry(QtCore.QRect(98, 56, 211, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")

        # 거래량 BTC
        self.label_5 = QtWidgets.QLabel(self.frame_3)
        self.label_5.setGeometry(QtCore.QRect(225, 56, 141, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")

        # 거래대금
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        self.label_2.setGeometry(QtCore.QRect(56, 84, 141, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        # 거래대금 Number
        self.label_6 = QtWidgets.QLabel(self.frame_3)
        self.label_6.setGeometry(QtCore.QRect(84, 84, 211, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")

        # 거래대금 백만원
        self.label_7 = QtWidgets.QLabel(self.frame_3)
        self.label_7.setGeometry(QtCore.QRect(232, 84, 141, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")

        # 최근24시간
        self.label_8 = QtWidgets.QLabel(self.frame_3)
        self.label_8.setGeometry(QtCore.QRect(162, 112, 211, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")

        # 구분선
        self.line = QtWidgets.QFrame(self.frame_3)
        self.line.setGeometry(QtCore.QRect(56, 141, 536, 22))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # 52주최고
        self.label_9 = QtWidgets.QLabel(self.frame_3)
        self.label_9.setGeometry(QtCore.QRect(56, 169, 141, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")

        # 52주최고 Number
        self.label_10 = QtWidgets.QLabel(self.frame_3)
        self.label_10.setGeometry(QtCore.QRect(162, 169, 211, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("color: RED;")
        self.label_10.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")

        # 52주최고 Date
        self.label_11 = QtWidgets.QLabel(self.frame_3)
        self.label_11.setGeometry(QtCore.QRect(162, 197, 211, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")

        # 52주최저
        self.label_14 = QtWidgets.QLabel(self.frame_3)
        self.label_14.setGeometry(QtCore.QRect(56, 239, 141, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")

        # 52주최저 Number
        self.label_12 = QtWidgets.QLabel(self.frame_3)
        self.label_12.setGeometry(QtCore.QRect(162, 239, 211, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("color: BLUE;")
        self.label_12.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")

        # 52주최저 Date
        self.label_13 = QtWidgets.QLabel(self.frame_3)
        self.label_13.setGeometry(QtCore.QRect(162, 267, 211, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")

        # 전일종가
        self.label_16 = QtWidgets.QLabel(self.frame_3)
        self.label_16.setGeometry(QtCore.QRect(457, 169, 141, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")

        # 전일종가 Number
        self.label_15 = QtWidgets.QLabel(self.frame_3)
        self.label_15.setGeometry(QtCore.QRect(562, 169, 211, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("")
        self.label_15.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")

        # 당일고가
        self.label_19 = QtWidgets.QLabel(self.frame_3)
        self.label_19.setGeometry(QtCore.QRect(457, 197, 141, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")

        # 당일고가 Number
        self.label_17 = QtWidgets.QLabel(self.frame_3)
        self.label_17.setGeometry(QtCore.QRect(562, 197, 211, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_17.setFont(font)
        self.label_17.setStyleSheet("color: RED;")
        self.label_17.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")

        # 당일최고등락률
        self.label_18 = QtWidgets.QLabel(self.frame_3)
        self.label_18.setGeometry(QtCore.QRect(562, 232, 211, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_18.setFont(font)
        self.label_18.setStyleSheet("color: RED;")
        self.label_18.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_18.setObjectName("label_18")

        # 당일저가
        self.label_22 = QtWidgets.QLabel(self.frame_3)
        self.label_22.setGeometry(QtCore.QRect(457, 267, 141, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")

        # 당일저가 Number
        self.label_20 = QtWidgets.QLabel(self.frame_3)
        self.label_20.setGeometry(QtCore.QRect(562, 267, 211, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_20.setFont(font)
        self.label_20.setStyleSheet("color: BLUE;")
        self.label_20.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")

        # 당일최저등락률
        self.label_21 = QtWidgets.QLabel(self.frame_3)
        self.label_21.setGeometry(QtCore.QRect(562, 302, 211, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_21.setFont(font)
        self.label_21.setStyleSheet("color: BLUE;")
        self.label_21.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_21.setObjectName("label_21")





        # 테이블 헤더: 파란색 매물
        self.label_40 = QtWidgets.QLabel(self.frame)
        self.label_40.setGeometry(QtCore.QRect(394, 842, 127, 49))
        self.label_40.setObjectName("label_40")
        self.label_40.setStyleSheet("border: 1px solid grey; background-color:white;")
        self.label_40.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        # 테이블 헤더: 수량
        self.button_quantity = QtWidgets.QPushButton(self.frame)
        self.button_quantity.setGeometry(QtCore.QRect(520, 842, 127, 49))
        self.button_quantity.setObjectName("button_quantity")
        self.button_quantity.setStyleSheet("border: 1px solid grey; background-color:white;")

        # 테이블 헤더: 빨간색 매물
        self.label_41 = QtWidgets.QLabel(self.frame)
        self.label_41.setGeometry(QtCore.QRect(647, 842, 127, 49))
        self.label_41.setObjectName("label_41")
        self.label_41.setStyleSheet("border: 1px solid grey; background-color:white;")
        self.label_41.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        # 테이블 헤더: 일괄취소(빨간색)
        self.button_cancel_2 = QtWidgets.QPushButton(self.frame)
        self.button_cancel_2.setGeometry(QtCore.QRect(773, 842, 127, 49))
        self.button_cancel_2.setObjectName("button_cancel_2")
        self.button_cancel_2.setStyleSheet("border: 1px solid grey; background-color:white; color: red;")

        # 왼쪽 메뉴 프레임
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 140, 1079))
        self.frame.setStyleSheet("background-color: rgb(50, 90, 160)")  # 배경색 설정
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # 메뉴-마이페이지 버튼
        self.menuButton_myPage_3 = QtWidgets.QPushButton(self.frame)
        self.menuButton_myPage_3.setGeometry(QtCore.QRect(29, 70, 84, 84))
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
        self.menuButton_trading_3 = QtWidgets.QPushButton(self.frame)
        self.menuButton_trading_3.setGeometry(QtCore.QRect(29, 210, 84, 84))
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
        self.menuButton_chart_3 = QtWidgets.QPushButton(self.frame)
        self.menuButton_chart_3.setGeometry(QtCore.QRect(29, 351, 84, 84))
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
        self.menuButton_autoTrading_3 = QtWidgets.QPushButton(self.frame)
        self.menuButton_autoTrading_3.setGeometry(QtCore.QRect(29, 491, 84, 84))
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
        self.menuButton_setting_3 = QtWidgets.QPushButton(self.frame)
        self.menuButton_setting_3.setGeometry(QtCore.QRect(29, 632, 84, 84))
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
        self.menuButton_exit_3 = QtWidgets.QPushButton(self.frame)
        self.menuButton_exit_3.setGeometry(QtCore.QRect(29, 913, 84, 84))
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
        self.label_coinName.setText("비트코인")
        self.label_coinNickname.setText("BTC/KRW")
        self.label_3.setText("호가")
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText("일괄취소")
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText("9,999")
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText("수량(BTC)")
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText("9,999")
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText("일괄취소")
        self.label.setText("거래량")
        self.label_2.setText("거래대금")
        self.label_4.setText("6,875")
        self.label_5.setText("BTC")
        self.label_6.setText("472,668")
        self.label_7.setText("백만원")
        self.label_8.setText("(최근 24시간)")
        self.label_9.setText("52주 최고")
        self.label_10.setText("81,994,000")
        self.label_11.setText("(2021.04.14)")
        self.label_12.setText("81,994,000")
        self.label_13.setText("(2021.04.14)")
        self.label_14.setText("52주 최저")
        self.label_15.setText("81,994,000")
        self.label_16.setText("전일종가")
        self.label_17.setText("81,994,000")
        self.label_19.setText("당일고가")
        self.label_20.setText("81,994,000")
        self.label_22.setText("당일저가")
        self.label_18.setText("+3.35%")
        self.label_21.setText("-0.37%")
        self.label_40.setText("9,999")
        self.label_41.setText("9,999")
        self.button_cancel_1.setText("일괄취소")
        self.button_cancel_2.setText("일괄취소")
        self.button_quantity.setText("수량(BTC)")
        self.reset()
        self.show()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    ui = Ui_MainWindow()
    sys.exit(app.exec_())
