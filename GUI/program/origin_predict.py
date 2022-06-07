from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import requests
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
import sys
import pandas as pd
import origin_module
import numpy as np

# 코인 실시간 데이터 불러오기
coin_url = "https://api.upbit.com/v1/market/all"
chart_url = "https://api.upbit.com/v1/ticker?markets="
headers = {"Accept": "application/json"}
response = requests.request("GET", coin_url, headers=headers)
print(response.text)
market_text = ""
current_coin = "KRW-BTC"
access_key = 'aaa'
secret_key = 'aaa'

class Ui_Predict(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setupUI()

        timer = QTimer(self)
        timer.start(1000)
        timer.timeout.connect(self.setData)
        
        url = "https://api.upbit.com/v1/market/all?isDetails=false"

        headers = {"Accept": "application/json"}

        response = requests.get(url, headers=headers)
        response = response.json()
        self.coin_list = []
        for i in response:
            if "KRW" in i["market"]:
                self.coin_list.append(i['market'])
    def lineeditTextFunction(self):
        tx = self.edit_search.text()
        tx = tx.upper()
        print(tx)
        print(1)
        coin_tmp = []
        for i in self.coin_list:
            if tx in i:
                coin_tmp.append(i)
        first = 0
        self.market_text = ''
        for i in coin_tmp:
            self.market_text += i+"%2C%20"
        self.market_text = self.default_market_text if self.market_text == '' else self.market_text[:-6]
        chart_res = requests.request("GET", 'https://api.upbit.com/v1/ticker?markets=' + self.market_text, headers=headers)
        df = pd.DataFrame(chart_res.json())
        new_df = pd.DataFrame()
        new_df["코인명"] = df["market"]
        new_df["현재가"] = df["trade_price"]
        new_df["전일대비"] = df["signed_change_price"]
        new_df["거래대금"] = round(df["acc_trade_price_24h"] / 1000000)

        new_df = new_df.sort_values(by='거래대금', ascending=False)
        new_df = new_df.reset_index(drop=True)
        cnt = len(new_df)
        # print("cnt: ", cnt)
        for k in range(cnt):
            self.tableWidget.setItem(k, 0, QTableWidgetItem(new_df['코인명'][k]))
            self.tableWidget.setItem(k, 1, QTableWidgetItem(str(new_df['현재가'][k])))
            self.tableWidget.setItem(k, 2, QTableWidgetItem(str(new_df['전일대비'][k])))
            self.tableWidget.setItem(k, 3, QTableWidgetItem(str("{:g}".format((new_df['거래대금'][k])) + " 백만")))

        self.tableWidget.setRowCount(len(new_df))
    # 코인 실시간 데이터 반영
    def setData(self):
        chart_res = requests.request("GET", chart_url + self.market_text, headers=headers)

        df = pd.DataFrame(chart_res.json())
        new_df = pd.DataFrame()
        new_df["코인명"] = df["market"]
        new_df["현재가"] = df["trade_price"]
        new_df["전일대비"] = df["signed_change_price"]
        new_df["거래대금"] = round(df["acc_trade_price_24h"] / 1000000)

        new_df = new_df.sort_values(by='거래대금', ascending=False)
        new_df = new_df.reset_index(drop=True)
        # print(new_df)

        cnt = len(new_df)
        # print("cnt: ", cnt)
        for k in range(cnt):
            self.tableWidget.setItem(k, 0, QTableWidgetItem(new_df['코인명'][k]))
            self.tableWidget.setItem(k, 1, QTableWidgetItem(str(new_df['현재가'][k])))
            self.tableWidget.setItem(k, 2, QTableWidgetItem(str(new_df['전일대비'][k])))
            self.tableWidget.setItem(k, 3, QTableWidgetItem(str("{:g}".format((new_df['거래대금'][k])) + " 백만")))

        self.tableWidget.setRowCount(len(new_df))

    def setupUI(self):
        # 전체 KRW 코인
        global market_text
        market_text = ''
        first = 0
        for i in response.json():
            if "KRW" in i["market"]:
                self.market_text += i["market"] + "%2C%20"
        self.market_text = self.market_text[:-6]
        # print(i["market"])
        self.default_market_text = self.market_text

        # print(market_text)

        global access_key, secret_key
        access_key = 'Da6POBtP1FxfCvphLxXicwkv2hvSKXkodJ5oaLxe'
        secret_key = 'vKWdRCJWGU7yycHPEmAj8tz5PvPtqvBz3HmfvSth'
        # access_key = origin_module.access_key
        # secret_key = origin_module.secret_key

        self.setObjectName("MainWindow")
        self.resize(1920, 1080)
        self.setInputMethodHints(QtCore.Qt.ImhNone)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: rgb(255,255,255)")

        # 왼쪽 프레임
        self.frame = QtWidgets.QMainWindow(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0,112,1546,1435))
        #self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        #self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.setStyleSheet("background-color:none;")

        # 호가창
        # self.chart = QLabel(self)
        # self.chart.setGeometry(QtCore.QRect(443, 150, 1700, 1100))
        # self.pixmap = QPixmap('resources/predict.jpg')
        # self.chart.setPixmap(self.pixmap)
        # self.chart.setContentsMargins(10,10,10,10)
        # self.chart.resize(self.pixmap.width(), self.pixmap.height())

        # 오른쪽 프레임
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setStyleSheet("background-color:none;")
        self.frame_2.setGeometry(QtCore.QRect(1534,0,960,1079))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        # # 검색창 돋보기 이미지
        # self.image_search = QtWidgets.QGraphicsView(self.frame_2)
        # self.image_search.setGeometry(QtCore.QRect(0,50,49,49))
        # self.image_search.setStyleSheet("border-image: url(resources/search.png); background-repeat: no-repeat;")
        # self.image_search.setObjectName("image_search")
        #
        # # 검색창
        # self.edit_search = QtWidgets.QLineEdit(self.frame_2)
        # self.edit_search.setGeometry(QtCore.QRect(53,50,297,49))
        # font = QtGui.QFont()
        # font.setPointSize(20)
        # self.edit_search.setFont(font)
        # self.edit_search.setObjectName("edit_search")

        # 검색창 돋보기 이미지
        self.image_search = QtWidgets.QGraphicsView(self.frame_2)
        self.image_search.setGeometry(QtCore.QRect(0, 120, 35, 35))
        self.image_search.setStyleSheet("border-image: url(resources/search.png); background-repeat: no-repeat;")
        self.image_search.setObjectName("image_search")

        # 검색창
        self.edit_search = QtWidgets.QLineEdit(self.frame_2)
        self.edit_search.setGeometry(QtCore.QRect(50, 120, 320, 35))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.edit_search.setFont(font)
        self.edit_search.setObjectName("edit_search")
        self.edit_search.textChanged.connect(self.lineeditTextFunction)
        # # 호가 테이블
        # self.tableWidget = QtWidgets.QTableWidget(self.frame_2)
        # self.tableWidget.setGeometry(QtCore.QRect(0,120,350,830))
        # self.tableWidget.setRowCount(36)  # 테이블 기본 행 갯수
        # self.tableWidget.setColumnCount(4)  # 테이블 기본 열 갯수
        # self.tableWidget.setObjectName("tableWidget")
        # item = QtWidgets.QTableWidgetItem()
        # self.tableWidget.setHorizontalHeaderItem(0, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.tableWidget.setHorizontalHeaderItem(1, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.tableWidget.setHorizontalHeaderItem(2, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.tableWidget.setHorizontalHeaderItem(3, item)
        # self.tableWidget.horizontalHeader().setStretchLastSection(False)
        # self.tableWidget.verticalHeader().setVisible(False)  # 수직헤더
        # self.tableWidget.horizontalHeader().setVisible(False)  # 수평헤더
        # self.tableWidget.horizontalHeader().setDefaultSectionSize(87)  # 테이블 기본 열 크기
        # self.tableWidget.verticalHeader().setDefaultSectionSize(20)  # 테이블 기본 행 크기

        # 전체 실시간 코인 테이블
        self.tableWidget = QtWidgets.QTableWidget(self.frame_2)
        self.tableWidget.setGeometry(QtCore.QRect(0, 180, 380, 700))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["코인명", "현재가", "전일대비", "거래대금"])
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        self.tableWidget.horizontalHeader().setFont(font)
        self.tableWidget.setFont(font)
        self.tableWidget.horizontalHeader().setStyleSheet(
            """
            QHeaderView::section {
                background-color:#F3F3F3;
                border-top: 0px;
                border-left: 0px;
                border-right: 0px;
                border-bottom: 1px solid #F3F3F3;
            }
            """
        )
        self.tableWidget.setStyleSheet("border: 1px solid #F3F3F3; border-bottom: 1px solid #F3F3F3;")

        # self.tableWidget.setStyleSheet("border: 3px;""border-color: #F3F3F3;")
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setFixedHeight(35)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(90)  # 테이블 기본 열 크기
        self.tableWidget.verticalHeader().setDefaultSectionSize(35)  # 테이블 기본 행 크기
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # edit 금지 모드
        self.tableWidget.verticalHeader().setVisible(False)  # 행 번호 안보이게 설정
        self.tableWidget.setSelectionMode(QAbstractItemView.NoSelection)  # 선택 불능
        self.tableWidget.doubleClicked.connect(self.coin_click_event)
        self.tableWidget.setShowGrid(False)  # grid line 숨기기


        # 왼쪽 메뉴 프레임
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0,0,140,1079))
        self.frame.setStyleSheet("background-color: rgb(50, 90, 160)")  # 배경색 설정
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # 메뉴-마이페이지 버튼
        self.menuButton_myPage_3 = QtWidgets.QPushButton(self.frame)
        self.menuButton_myPage_3.setGeometry(QtCore.QRect(30, 70, 84, 84))
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
        self.menuButton_myPage_3.clicked.connect(self.button_mypage_event)

        # 메뉴-트레이딩 버튼
        self.menuButton_trading_3 = QtWidgets.QPushButton(self.frame)
        self.menuButton_trading_3.setGeometry(QtCore.QRect(30, 211, 84, 84))
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
        # self.menuButton_trading_3.clicked.connect(origin_module.event.button_trade_event)
        self.menuButton_trading_3.clicked.connect(self.button_trade_event)

        # 메뉴-거래(사고팔기) 버튼 (실시간차트)
        self.menuButton_chart_3 = QtWidgets.QPushButton(self.frame)
        self.menuButton_chart_3.setGeometry(QtCore.QRect(30, 351, 84, 84))
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
        self.menuButton_chart_3.clicked.connect(self.button_chart_event)

        # 메뉴-자동거래 버튼
        self.menuButton_autoTrading_3 = QtWidgets.QPushButton(self.frame)
        self.menuButton_autoTrading_3.setGeometry(QtCore.QRect(30, 492, 84, 84))
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
        self.menuButton_autoTrading_3.clicked.connect(self.button_auto_event)

        # 변동성 예측 버튼
        self.menuButton_predict_3 = QtWidgets.QPushButton(self.frame)
        self.menuButton_predict_3.setGeometry(QtCore.QRect(30, 633, 84, 84))
        self.menuButton_predict_3.setObjectName("menuButton_trading_3")
        self.menuButton_predict_3.setStyleSheet(
            """
            QPushButton {
                border-image: url(resources/predict.png);
                background-repeat: no-repeat;
            }
            QPushButton:pressed {
                border-image: url(resources/predict_clicked.png);
                background-repeat: no-repeat;
            }
            """
        )
        self.menuButton_predict_3.clicked.connect(self.button_predict_event)

        # 메뉴-환경설정 버튼
        self.menuButton_setting_3 = QtWidgets.QPushButton(self.frame)
        self.menuButton_setting_3.setGeometry(QtCore.QRect(30, 774, 84, 84))
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
        self.menuButton_setting_3.clicked.connect(self.button_setup_event)

        # 메뉴-로그아웃 버튼
        self.menuButton_exit_3 = QtWidgets.QPushButton(self.frame)
        self.menuButton_exit_3.setGeometry(QtCore.QRect(30, 914, 84, 84))
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
        self.menuButton_exit_3.clicked.connect(self.button_close_event)


        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def coin_click_event(self):
        global current_coin
        current_coin = self.tableWidget.currentIndex().data()
        self.webEngineView.setUrl(QtCore.QUrl("https://upbit.com/full_chart?code=CRIX.UPBIT."+current_coin))

    def button_trade_event(self):
        origin_module.predict_check = 0
        origin_module.trade_check = 1
        self.close()
        win = origin_module.Ui_Trading()
        r = win.showModal()
        # self.close()

    def button_chart_event(self):
        origin_module.predict_check = 0
        origin_module.chart_check = 1
        self.close()
        win = origin_module.Ui_Chart()
        r = win.showModal()
        # self.close()

    def button_auto_event(self):
        origin_module.predict_check = 0
        self.close()
        win = origin_module.Ui_Auto()
        r = win.showModal()
        # self.close()

    def button_predict_event(self):
        origin_module.predict_check = 1
        self.close()
        win = origin_module.Ui_Predict()
        r = win.showModal()
        # self.close()

    def button_mypage_event(self):
        origin_module.predict_check = 0
        self.close()
        win = origin_module.Ui_MyPage()
        # self.close()
        r = win.showModal()
        # self.close()

    def button_close_event(self):
        self.close()

    def button_setup_event(self):
        origin_module.predict_check = 0
        self.close()
        win = origin_module.Ui_Setup()
        r = win.showModal()
        # self.close()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def showModal(self):
        return super().exec_()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Ui_Predict()
    win.setWindowTitle('HYCOIN')
    #win.showMaximized()
    win.show()
    sys.exit(app.exec_())
