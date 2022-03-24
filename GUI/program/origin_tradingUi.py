from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import uuid
import jwt
import cx_Oracle
import requests
import origin_module

Connect = cx_Oracle.connect("hycoin/hycoin1234@hycoin.crmeanf0td5o.ap-northeast-2.rds.amazonaws.com:1521/HYCOIN")
Cursor = Connect.cursor()

# access_key = 'zSbtYUz3KVLnBa3n4LqNPOQCJxT6hdDtgEiyyLsa'
# secret_key = 'xJmMQby5D7RepbxVGBmXTQ7Jh95jxahCJNEtM7Mx'
access_key = 'aaa'
secret_key = 'aaa'
server_url = 'https://api.upbit.com'
coin_name_url = 'https://api.upbit.com/v1/market/all'

# payload = {
#     'access_key': access_key,
#     'nonce': str(uuid.uuid4()),
# }
#
# jwt_token = jwt.encode(payload, secret_key)
# authorize_token = 'Bearer {}'.format(jwt_token)
# headers = {"Authorization": authorize_token}
#
# res = requests.get(server_url + "/v1/accounts", headers=headers)
# json_data = res.json()
# print(json_data)

class Ui_Trading(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        global access_key, secret_key
        access_key = origin_module.access_key
        secret_key = origin_module.secret_key

        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
        }

        jwt_token = jwt.encode(payload, secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.get(server_url + "/v1/accounts", headers=headers)
        json_data = res.json()
        print(json_data)

        self.setObjectName("MainWindow")
        self.resize(1920, 1080)
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

        # 검색창
        self.edit_search = QtWidgets.QLineEdit(self.centralwidget)
        self.edit_search.setGeometry(QtCore.QRect(267, 56, 675, 49))
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
        self.frame.setGeometry(QtCore.QRect(0, 0, 141, 1079))
        self.frame.setStyleSheet("background-color: rgb(50, 90, 160)")  # 배경색 설정
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

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
        self.label_coinNickname.setGeometry(QtCore.QRect(422, 4, 211, 98))
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
        self.tableWidget.setGeometry(QtCore.QRect(267, 141, 675, 751))
        self.tableWidget.setRowCount(20) # 테이블 기본 행 갯수
        self.tableWidget.setColumnCount(5) # 테이블 기본 열 갯수
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
        self.tableWidget.verticalHeader().setVisible(False) # 수직헤더
        self.tableWidget.horizontalHeader().setVisible(False)  # 수평헤더
        self.tableWidget.horizontalHeader().setDefaultSectionSize(90)  # 테이블 기본 열 크기
        self.tableWidget.verticalHeader().setDefaultSectionSize(35)  # 테이블 기본 행 크기

        # 테이블 헤더: 일괄취소(파란색)
        self.button_cancel_1 = QtWidgets.QPushButton(self.frame)
        self.button_cancel_1.setGeometry(QtCore.QRect(267, 842, 128, 49))
        self.button_cancel_1.setObjectName("button_cancel_1")
        self.button_cancel_1.setStyleSheet("border: 1px solid grey; background-color:white; color: blue;")

        # 테이블 헤더: 파란색 매물
        self.label_40 = QtWidgets.QLabel(self.frame)
        self.label_40.setGeometry(QtCore.QRect(394, 842, 128, 49))
        self.label_40.setObjectName("label_40")
        self.label_40.setStyleSheet("border: 1px solid grey; background-color:white;")
        self.label_40.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        # 테이블 헤더: 수량
        self.button_quantity = QtWidgets.QPushButton(self.frame)
        self.button_quantity.setGeometry(QtCore.QRect(520, 842, 128, 49))
        self.button_quantity.setObjectName("button_quantity")
        self.button_quantity.setStyleSheet("border: 1px solid grey; background-color:white;")

        # 테이블 헤더: 빨간색 매물
        self.label_41 = QtWidgets.QLabel(self.frame)
        self.label_41.setGeometry(QtCore.QRect(647, 842, 128, 49))
        self.label_41.setObjectName("label_41")
        self.label_41.setStyleSheet("border: 1px solid grey; background-color:white;")
        self.label_41.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


        # 테이블 헤더: 일괄취소(빨간색)
        self.button_cancel_2 = QtWidgets.QPushButton(self.frame)
        self.button_cancel_2.setGeometry(QtCore.QRect(773, 842, 128, 49))
        self.button_cancel_2.setObjectName("button_cancel_2")
        self.button_cancel_2.setStyleSheet("border: 1px solid grey; background-color:white; color: red;")

        # 오른쪽 프레임
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setStyleSheet("background-color:none;")
        self.frame_2.setGeometry(QtCore.QRect(984, 0, 960, 1079))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")


        # 보유종목
        self.comboBox = QtWidgets.QComboBox(self.frame_2)
        self.comboBox.setGeometry(QtCore.QRect(84, 56, 281, 49))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("보유종목")
        for i in json_data :
            if i["currency"] != "KRW":
                print(i["currency"])
                self.comboBox.addItem(i["currency"])
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.comboBox.setFont(font)

        # 종목정보 Frame
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setStyleSheet("background-color:none;")
        self.frame_3.setGeometry(QtCore.QRect(28, 98, 1323, 550))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")

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
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")

        # 최근24시간
        self.label_8 = QtWidgets.QLabel(self.frame_3)
        self.label_8.setGeometry(QtCore.QRect(162, 112, 211, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
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
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")

        # 52주최고 Date
        self.label_11 = QtWidgets.QLabel(self.frame_3)
        self.label_11.setGeometry(QtCore.QRect(162, 197, 211, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
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
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")

        # 52주최저 Date
        self.label_13 = QtWidgets.QLabel(self.frame_3)
        self.label_13.setGeometry(QtCore.QRect(162, 267, 211, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")

        # 전일종가
        self.label_16 = QtWidgets.QLabel(self.frame_3)
        self.label_16.setGeometry(QtCore.QRect(457, 169, 141, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")

        #전일종가 Number
        self.label_15 = QtWidgets.QLabel(self.frame_3)
        self.label_15.setGeometry(QtCore.QRect(562, 169, 211, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("")
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
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
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
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
        self.label_20.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")

        # 당일최저등락률
        self.label_21 = QtWidgets.QLabel(self.frame_3)
        self.label_21.setGeometry(QtCore.QRect(562, 302, 211, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_21.setFont(font)
        self.label_21.setStyleSheet("color: BLUE;")
        self.label_21.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_21.setObjectName("label_21")

        # 매수버튼
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setGeometry(QtCore.QRect(84, 450, 246, 84))
        self.pushButton.setObjectName("pushButton")

        # 매도버튼
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_2.setGeometry(QtCore.QRect(323, 450, 246, 84))
        self.pushButton_2.setObjectName("pushButton_2")

        #거래내역
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_3.setGeometry(QtCore.QRect(562, 450, 246, 84))
        self.pushButton_3.setObjectName("pushButton_3")

        # 매수매도거래내역 프레임
        self.frame_order = QtWidgets.QFrame(self.frame_2)
        self.frame_order.setGeometry(QtCore.QRect(84, 527, 724, 492))
        self.frame_order.setStyleSheet("background-color:grey;")
        self.frame_order.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_order.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_order.setObjectName("frame_order")

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

#         self.setCentralWidget(self.centralwidget)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    # def button_myPage_event(self):
    #     widget.setCurrentIndex(widget.currentIndex() + 1)

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
        self.label_coinName.setText(_translate("MainWindow", "비트코인"))
        self.label_coinNickname.setText(_translate("MainWindow", "BTC/KRW"))
        self.label_3.setText(_translate("MainWindow", "호가"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "일괄취소"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "9,999"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "수량(BTC)"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "9,999"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "일괄취소"))
        self.label.setText(_translate("MainWindow", "거래량"))
        self.label_2.setText(_translate("MainWindow", "거래대금"))
        self.label_4.setText(_translate("MainWindow", "6,875"))
        self.label_5.setText(_translate("MainWindow", "BTC"))
        self.label_6.setText(_translate("MainWindow", "472,668"))
        self.label_7.setText(_translate("MainWindow", "백만원"))
        self.label_8.setText(_translate("MainWindow", "(최근 24시간)"))
        self.label_9.setText(_translate("MainWindow", "52주 최고"))
        self.label_10.setText(_translate("MainWindow", "81,994,000"))
        self.label_11.setText(_translate("MainWindow", "(2021.04.14)"))
        self.label_12.setText(_translate("MainWindow", "81,994,000"))
        self.label_13.setText(_translate("MainWindow", "(2021.04.14)"))
        self.label_14.setText(_translate("MainWindow", "52주 최저"))
        self.label_15.setText(_translate("MainWindow", "81,994,000"))
        self.label_16.setText(_translate("MainWindow", "전일종가"))
        self.label_17.setText(_translate("MainWindow", "81,994,000"))
        self.label_19.setText(_translate("MainWindow", "당일고가"))
        self.label_20.setText(_translate("MainWindow", "81,994,000"))
        self.label_22.setText(_translate("MainWindow", "당일저가"))
        self.label_18.setText(_translate("MainWindow", "+3.35%"))
        self.label_21.setText(_translate("MainWindow", "-0.37%"))
        self.label_40.setText(_translate("MainWindow", "9,999"))
        self.label_41.setText(_translate("MainWindow", "9,999"))
        self.button_cancel_1.setText(_translate("MainWindow", "일괄취소"))
        self.button_cancel_2.setText(_translate("MainWindow", "일괄취소"))
        self.button_quantity.setText(_translate("MainWindow", "수량(BTC)"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_3.setText(_translate("MainWindow", "PushButton"))

    def showModal(self):
        return super().exec_()

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     import myPageUi
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     # 화면 전환용 widget
#     widget = QtWidgets.QStackedWidget()
#
#     # 거래 widget
#     trade = QtWidgets.QMainWindow()
#     ui2 = Ui_MainWindow()
#     ui2.setupUi(trade)
#     widget.addWidget(trade)
#
#     # 마이페이지 widget
#     myPage = QtWidgets.QMainWindow()
#     ui = myPageUi.Ui_MyPage()
#     ui.setupUI(myPage)
#     widget.addWidget(myPage)
#
#     widget.show()
#     app.exec_()

# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     win = Ui_Trading()
#     win.show()
#     sys.exit(app.exec_())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Ui_Trading()
    win.setWindowTitle('HYCOIN')
    #win.showMaximized()
    win.show()
    sys.exit(app.exec_())