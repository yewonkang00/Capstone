from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import sys
import requests
from PyQt5.QtCore import Qt, QTime, QTimer
from PyQt5.QtWidgets import *
import pandas as pd
import time
import origin_module

# 코인 실시간 데이터 불러오기
coin_url = "https://api.upbit.com/v1/market/all"
chart_url = "https://api.upbit.com/v1/ticker?markets="
headers = {"Accept": "application/json"}
response = requests.request("GET", coin_url, headers=headers)
market_text = ""
access_key = 'aaa'
secret_key = 'aaa'
first = 0

# 전체 KRW 코인
for i in response.json():
    if "KRW" in i["market"]:
        if(first == 0):
            market_text += i["market"]
            first = 1
        else :
            market_text += "%2C%20"
            market_text += i["market"]

print(market_text)

class Ui_Chart(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        global access_key, secret_key
        access_key = origin_module.access_key
        secret_key = origin_module.secret_key

        self.setObjectName("MainWindow")
        self.resize(1920, 1080)
        # self.setFixedSize(1920, 1080)
        self.setInputMethodHints(QtCore.Qt.ImhNone)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: rgb(255,255,255)")

        # 전체프레임
        self.full_frame = QtWidgets.QFrame(self.centralwidget)
        self.full_frame.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.full_frame.setMouseTracking(True)
        self.full_frame.setAutoFillBackground(False)
        self.full_frame.setStyleSheet("background-color: rgb(255,255,255)")
        self.full_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.full_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.full_frame.setMidLineWidth(0)
        self.full_frame.setObjectName("full_frame")

        # 왼쪽 프레임
        # self.frame = QtWidgets.QFrame(self.centralwidget)
        # self.frame.setGeometry(QtCore.QRect(0, 80, 981, 1021))
        # self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame.setObjectName("frame")
        # self.frame.setStyleSheet("background-color:none;")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 141, 1079))
        self.frame.setStyleSheet("background-color: rgb(50, 90, 160)")  # 배경색 설정
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # 실시간 차트
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.full_frame)
        self.webEngineView.setGeometry(QtCore.QRect(175, 140, 1300, 750))
        self.webEngineView.setUrl(QtCore.QUrl("https://upbit.com/full_chart?code=CRIX.UPBIT.KRW-BTC"))

        # 매수 버튼
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(750, 90, 70, 38))
        self.pushButton_3.setObjectName("pushButton_3")
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setFamily("Malgun Gothic")
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("border: 1px solid white; background-color:red; color: white;")

        # 매도 버튼
        self.pushButton_4 = QtWidgets.QPushButton(self.frame)
        self.pushButton_4.setGeometry(QtCore.QRect(820, 90, 70, 38))
        self.pushButton_4.setObjectName("pushButton_4")
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setFamily("Malgun Gothic")
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("border: 1px solid white; background-color:blue; color: white;")

        # 오른쪽 프레임
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setStyleSheet("background-color:none;")
        self.frame_2.setGeometry(QtCore.QRect(1534,0,960,1079))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        # 검색창 돋보기 이미지
        self.image_search = QtWidgets.QGraphicsView(self.frame_2)
        self.image_search.setGeometry(QtCore.QRect(0, 80, 35, 35))
        self.image_search.setStyleSheet("border-image: url(resources/search.png); background-repeat: no-repeat;")
        self.image_search.setObjectName("image_search")

        # 검색창
        self.edit_search = QtWidgets.QLineEdit(self.frame_2)
        self.edit_search.setGeometry(QtCore.QRect(50, 80, 320, 35))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.edit_search.setFont(font)
        self.edit_search.setObjectName("edit_search")

        # 전체 실시간 코인 테이블
        self.tableWidget = QtWidgets.QTableWidget(self.frame_2)
        self.tableWidget.setGeometry(QtCore.QRect(0, 140, 380, 544))
        self.tableWidget.setColumnCount(4)

        # self.timer = QTimer(self)
        # self.timer.start(10000)
        # self.timer.timeout.connect(self.setData())
        #################
        # 전체 KRW 코인의 정보

        # while True:
        #     chart_res = requests.request("GET", chart_url + market_text, headers=chart_headers)
        #
        #     df = pd.DataFrame(chart_res.json())
        #     new_df = pd.DataFrame()
        #     new_df["코인명"] = df["market"]
        #     new_df["현재가"] = df["trade_price"]
        #     new_df["전일대비"] = df["signed_change_price"]
        #     new_df["거래대금"] = round(df["acc_trade_price_24h"] / 1000000)
        #
        #     new_df = new_df.sort_values(by='거래대금', ascending=False)
        #     new_df = new_df.reset_index(drop=True)
        #     print(new_df)
        #
        #     time.sleep(10)
        #
        #     cnt = len(new_df)
        #     print("cnt: ", cnt)
        #     for i in range(cnt):
        #         self.tableWidget.setItem(i, 0, QTableWidgetItem(new_df['코인명'][i]))
        #         self.tableWidget.setItem(i, 1, QTableWidgetItem(str(new_df['현재가'][i])))
        #         self.tableWidget.setItem(i, 2, QTableWidgetItem(str("{:g}".format((new_df['전일대비'][i])))))
        #         self.tableWidget.setItem(i, 3, QTableWidgetItem(str("{:g}".format((new_df['거래대금'][i])))))
        ##################

        # self.tableWidget.setRowCount(len(new_df))

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
        self.tableWidget.setShowGrid(False)  # grid line 숨기기



        # for i in range (cnt) :
        #     print(new_df['현재가'][i])
        #     print(int(new_df['현재가'][i]))
        #     self.tableWidget.setItem(i, 1, QTableWidgetItem(int(new_df['현재가'][i])))

        # 왼쪽 메뉴 프레임
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 141, 1079))
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

        # 메뉴-환경설정 버튼
        self.menuButton_setting_3 = QtWidgets.QPushButton(self.frame)
        self.menuButton_setting_3.setGeometry(QtCore.QRect(30, 633, 84, 84))
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
        self.menuButton_setting_3.clicked.connect(self.button_close_event)

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

       # self.setCentralWidget(self.centralwidget)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    # def setData(self):
    #     while True:
    #         chart_res = requests.request("GET", chart_url + market_text, headers=chart_headers)
    #
    #         df = pd.DataFrame(chart_res.json())
    #         new_df = pd.DataFrame()
    #         new_df["코인명"] = df["market"]
    #         new_df["현재가"] = df["trade_price"]
    #         new_df["전일대비"] = df["signed_change_price"]
    #         new_df["거래대금"] = round(df["acc_trade_price_24h"] / 1000000)
    #
    #         new_df = new_df.sort_values(by='거래대금', ascending=False)
    #         new_df = new_df.reset_index(drop=True)
    #         print(new_df)
    #
    #         time.sleep(10)
    #
    #         cnt = len(new_df)
    #         print("cnt: ", cnt)
    #         self.tableWidget.setItem(i, 0, QTableWidgetItem(new_df['코인명'][i]))
    #         self.tableWidget.setItem(i, 1, QTableWidgetItem(str(new_df['현재가'][i])))
    #         self.tableWidget.setItem(i, 2, QTableWidgetItem(str("{:g}".format((new_df['전일대비'][i])))))
    #         self.tableWidget.setItem(i, 3, QTableWidgetItem(str("{:g}".format((new_df['거래대금'][i])))))
    #
    #         self.tableWidget.setRowCount(len(new_df))

    def button_trade_event(self):
        win = origin_module.Ui_Trading()
        r = win.showModal()
        self.close()

    def button_chart_event(self):
        win = origin_module.Ui_Chart()
        r = win.showModal()
        self.close()

    def button_auto_event(self):
        win = origin_module.Ui_Auto()
        r = win.showModal()
        self.close()

    def button_mypage_event(self):
        win = origin_module.Ui_MyPage()
        # self.close()
        r = win.showModal()
        self.close()

    def button_close_event(self):
        self.close()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        # self.label_coinName.setText(_translate("MainWindow", "비트코인"))
        # self.label_coinNickname.setText(_translate("MainWindow", "BTC/KRW"))
        # self.label_3.setText(_translate("MainWindow", "호가"))
        # item = self.tableWidget.horizontalHeaderItem(0)
        # item.setText(_translate("MainWindow", "일괄취소"))
        # item = self.tableWidget.horizontalHeaderItem(1)
        # item.setText(_translate("MainWindow", "9,999"))
        # item = self.tableWidget.horizontalHeaderItem(2)
        # item.setText(_translate("MainWindow", "수량(BTC)"))
        # item = self.tableWidget.horizontalHeaderItem(3)
        # item.setText(_translate("MainWindow", "9,999"))
        # item = self.tableWidget.horizontalHeaderItem(4)
        # item.setText(_translate("MainWindow", "일괄취소"))
        # self.label.setText(_translate("MainWindow", "거래량"))
        # self.label_2.setText(_translate("MainWindow", "거래대금"))
        # self.label_4.setText(_translate("MainWindow", "6,875"))
        # self.label_5.setText(_translate("MainWindow", "BTC"))
        # self.label_6.setText(_translate("MainWindow", "472,668"))
        # self.label_7.setText(_translate("MainWindow", "백만원"))
        # self.label_8.setText(_translate("MainWindow", "(최근 24시간)"))
        # self.label_9.setText(_translate("MainWindow", "52주 최고"))
        # self.label_10.setText(_translate("MainWindow", "81,994,000"))
        # self.label_11.setText(_translate("MainWindow", "(2021.04.14)"))
        # self.label_12.setText(_translate("MainWindow", "81,994,000"))
        # self.label_13.setText(_translate("MainWindow", "(2021.04.14)"))
        # self.label_14.setText(_translate("MainWindow", "52주 최저"))
        # self.label_15.setText(_translate("MainWindow", "81,994,000"))
        # self.label_17.setText(_translate("MainWindow", "81,994,000"))
        # self.label_19.setText(_translate("MainWindow", "당일고가"))
        # self.label_20.setText(_translate("MainWindow", "81,994,000"))
        # self.label_22.setText(_translate("MainWindow", "당일저가"))
        # self.label_18.setText(_translate("MainWindow", "+3.35%"))
        # self.label_21.setText(_translate("MainWindow", "-0.37%"))
        # self.label_40.setText(_translate("MainWindow", "9,999"))
        # self.label_41.setText(_translate("MainWindow", "9,999"))
        # self.button_cancel_1.setText(_translate("MainWindow", "일괄취소"))
        # self.button_cancel_2.setText(_translate("MainWindow", "일괄취소"))
        # self.button_quantity.setText(_translate("MainWindow", "수량(BTC)"))
        # self.pushButton.setText(_translate("MainWindow", "일"))
        # self.pushButton_1.setText(_translate("MainWindow", "주"))
        # self.pushButton_2.setText(_translate("MainWindow", "월"))
        self.pushButton_3.setText(_translate("MainWindow", "매수"))
        self.pushButton_4.setText(_translate("MainWindow", "매도"))
        # self.label_101.setText(_translate("MainWindow", "81,994,000"))
        # self.label_102.setText(_translate("MainWindow", "KRW"))
        # self.label_103.setText(_translate("MainWindow", "전일대비"))
        # self.label_104.setText(_translate("MainWindow", "+0.91%▲ 610,000"))
        # self.label_105.setText(_translate("MainWindow", "고가"))
        # self.label_106.setText(_translate("MainWindow", "68,280,000"))
        # self.label_107.setText(_translate("MainWindow", "거래량(24H)"))
        # self.label_108.setText(_translate("MainWindow", "7,052.103 BTC"))
        # self.label_109.setText(_translate("MainWindow", "저가"))
        # self.label_110.setText(_translate("MainWindow", "66,350,000"))
        # self.label_111.setText(_translate("MainWindow", "거래대금(24H)"))
        # self.label_112.setText(_translate("MainWindow", "484, 272,350,212 KRW"))

        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "코인명"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "현재가"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "전일대비"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "거래대금"))
        item.setBackground(Qt.gray)

    def showModal(self):
        return super().exec_()

# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     win = QtWidgets.QMainWindow()
#     win = Ui_Chart()
#     win.show()
#     sys.exit(app.exec_())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Ui_Chart()
    win.setWindowTitle('HYCOIN')
    win.showMaximized()
    win.show()
    sys.exit(app.exec_())