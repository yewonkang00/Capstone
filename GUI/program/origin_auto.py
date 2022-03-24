from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import sys
import uuid
import jwt
import cx_Oracle
import requests
import origin_module

Connect = cx_Oracle.connect("hycoin/hycoin1234@hycoin.crmeanf0td5o.ap-northeast-2.rds.amazonaws.com:1521/HYCOIN")
Cursor = Connect.cursor()

access_key = 'aaa'
secret_key = 'aaa'
money_text = ''
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
# print("*",json_data)
# print("this is ripple: ",json_data[1]["unit_currency"]+"-"+json_data[1]["currency"])
#
# # 주문 가능 금액
# money = int(float(json_data[0]["balance"]))
# print(money)
# money_text = str(money) + "   KRW"

class Ui_Auto(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        global access_key, secret_key
        access_key = origin_module.access_key
        secret_key = origin_module.secret_key

        access_key = 'zSbtYUz3KVLnBa3n4LqNPOQCJxT6hdDtgEiyyLsa'
        secret_key = 'xJmMQby5D7RepbxVGBmXTQ7Jh95jxahCJNEtM7Mx'

        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
        }

        jwt_token = jwt.encode(payload, secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.get(server_url + "/v1/accounts", headers=headers)
        json_data = res.json()
        print("*", json_data)
        print("this is ripple: ", json_data[1]["unit_currency"] + "-" + json_data[1]["currency"])

        # 주문 가능 금액
        money = int(float(json_data[0]["balance"]))
        print(money)
        global money_text
        money_text = str(money) + "   KRW"

        self.setObjectName("MainWindow")
        self.resize(1920, 1080)
        self.setInputMethodHints(QtCore.Qt.ImhNone)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: rgb(255,255,255)")

        # 검색창
        self.edit_search = QtWidgets.QLineEdit(self.centralwidget)
        self.edit_search.setGeometry(QtCore.QRect(238,56,674,49))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.edit_search.setFont(font)
        self.edit_search.setObjectName("edit_search")

        # 검색창 돋보기 이미지
        self.image_search = QtWidgets.QGraphicsView(self.centralwidget)
        self.image_search.setGeometry(QtCore.QRect(175,56,49,49))
        self.image_search.setStyleSheet("border-image: url(resources/search.png); background-repeat: no-repeat;")
        self.image_search.setObjectName("image_search")

        # 왼쪽 프레임
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 112, 1534, 1435))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.setStyleSheet("background-color:none;")

        # 실시간 차트
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.frame)
        self.webEngineView.setGeometry(QtCore.QRect(175, 0, 1300, 750))
        # print("this is ripple: " + json_data[1]("currency"))
        self.webEngineView.setUrl(QtCore.QUrl("https://upbit.com/full_chart?code=CRIX.UPBIT."+json_data[1]["unit_currency"]+"-"+json_data[1]["currency"]))

        # 과거 데이터 테스트
        self.back_trading = QtWidgets.QLabel(self.frame)
        self.back_trading.setGeometry(QtCore.QRect(175,750,281,70))
        self.back_trading.setObjectName("back_trading")
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setFamily("Malgun Gothic")
        self.back_trading.setFont(font)

        # 전략 선택
        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setGeometry(QtCore.QRect(350,765,182,49))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("  터틀 전략")
        self.comboBox.addItem("  전략 2번")
        self.comboBox.addItem("  전략 3번")
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setFamily("Malgun Gothic")
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet("border: 1px solid blue; background-color:white; color: black;")

        # 일 버튼
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(576,765,56,53))
        self.pushButton.setObjectName("pushButton")
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setFamily("Malgun Gothic")
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("border: 1px solid grey; background-color:blue; color: white;")

        # 주 버튼
        self.pushButton_1 = QtWidgets.QPushButton(self.frame)
        self.pushButton_1.setGeometry(QtCore.QRect(639,765,56,53))
        self.pushButton_1.setObjectName("pushButton_1")
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setFamily("Malgun Gothic")
        self.pushButton_1.setFont(font)
        self.pushButton_1.setStyleSheet("border: 1px solid grey; background-color:blue; color: white;")

        # 월 버튼
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(702,765,56,53))
        self.pushButton_2.setObjectName("pushButton_2")
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setFamily("Malgun Gothic")
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("border: 1px solid grey; background-color:blue; color: white;")

        # 년 버튼
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(765,765,56,53))
        self.pushButton_3.setObjectName("pushButton_3")
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setFamily("Malgun Gothic")
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("border: 1px solid grey; background-color:blue; color: white;")

        # 테스트 버튼
        self.pushButton_4 = QtWidgets.QPushButton(self.frame)
        self.pushButton_4.setGeometry(QtCore.QRect(899,765,98,53))
        self.pushButton_4.setObjectName("pushButton_4")
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setFamily("Malgun Gothic")
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("border: 1px solid blue; background-color:white; color: blue;")

        # 수익률
        self._yield = QtWidgets.QLabel(self.frame)
        self._yield.setGeometry(QtCore.QRect(1067,750,281,70))
        self._yield.setObjectName("_yield")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self._yield.setFont(font)

        # 오른쪽 프레임
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setStyleSheet("background-color:none;")
        self.frame_2.setGeometry(QtCore.QRect(1534,0,960,1079))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")


        # 보유종목
        # self.comboBox1 = QtWidgets.QComboBox(self.frame_2)
        # self.comboBox1.setGeometry(QtCore.QRect(30,90,182,49))
        # self.comboBox1.setObjectName("comboBox1")
        # self.comboBox1.addItem("보유종목")
        # self.comboBox1.addItem("doge")
        # self.comboBox1.addItem("btc")
        # font = QtGui.QFont()
        # font.setPointSize(12)
        # font.setBold(True)
        # self.comboBox1.setFont(font)
        # self.comboBox1.setStyleSheet("border: 1px solid blue; background-color:white; color: black;")
        #

        self.comboBox1 = QtWidgets.QComboBox(self.frame_2)
        self.comboBox1.setGeometry(QtCore.QRect(30,90,182,49))
        self.comboBox1.setObjectName("comboBox1")
        self.comboBox1.addItem("보유종목")
        for i in json_data :
            if i["currency"] != "KRW":
                print(i["currency"])
                self.comboBox1.addItem(i["currency"])
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.comboBox1.setFont(font)
        self.comboBox1.setStyleSheet("border: 1px solid blue; background-color:white; color: black;")
        self.comboBox1.activated[str].connect(self.selectedComboItem)

        # 주문가능
        self.label_114 = QtWidgets.QLabel(self.frame_2)
        self.label_114.setGeometry(QtCore.QRect(20,170,281,70))
        self.label_114.setObjectName("label_114")
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        self.label_114.setFont(font)

        # 주문금액
        self.label_115 = QtWidgets.QLabel(self.frame_2)
        self.label_115.setGeometry(QtCore.QRect(250,170,281,70))
        self.label_115.setObjectName("label_115")
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setFamily("Malgun Gothic")
        font.setBold(True)
        self.label_115.setFont(font)

        # 10%
        self.pushButton_5 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_5.setGeometry(QtCore.QRect(20,240,56,30))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setStyleSheet("border: 1px solid grey; background-color:white; color: black;")
        # 20%
        self.pushButton_6 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_6.setGeometry(QtCore.QRect(85,240,56,30))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.setStyleSheet("border: 1px solid grey; background-color:white; color: black;")
        # 50%
        self.pushButton_7 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_7.setGeometry(QtCore.QRect(150,240,56,30))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.setStyleSheet("border: 1px solid grey; background-color:white; color: black;")
        # 100%
        self.pushButton_8 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_8.setGeometry(QtCore.QRect(215,240,56,30))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.setStyleSheet("border: 1px solid grey; background-color:white; color: black;")
        # 직접입력
        self.pushButton_9 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_9.setGeometry(QtCore.QRect(280,240,84,30))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_9.setStyleSheet("border: 1px solid grey; background-color:white; color: black;")

        # 주문총액
        self.label_116 = QtWidgets.QLabel(self.frame_2)
        self.label_116.setGeometry(QtCore.QRect(20,280,281,70))
        self.label_116.setObjectName("label_116")
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_116.setFont(font)

        # 주문 금액
        self.edit_search_1 = QtWidgets.QLineEdit(self.frame_2)
        self.edit_search_1.setGeometry(QtCore.QRect(120,295,240,40))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.edit_search_1.setFont(font)
        self.edit_search_1.setObjectName("edit_search_1")


        #자동 매매 시작
        self.pushButton_10 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_10.setGeometry(QtCore.QRect(20,360,160,40))
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_10.setStyleSheet("border: 1px solid grey; background-color:red; color: white;")
        # 자동 매매 종료
        self.pushButton_11 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_11.setGeometry(QtCore.QRect(210,360,160,40))
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_11.setStyleSheet("border: 1px solid grey; background-color:blue; color: white;")



        # 자동 매매 거래 내역
        self.label_117 = QtWidgets.QLabel(self.frame_2)
        self.label_117.setGeometry(QtCore.QRect(7,430,281,70))
        self.label_117.setObjectName("label_117")
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_117.setFont(font)

        # 자동매매 거래 내역 리스트
        self.table_currentCoinList = QtWidgets.QTableWidget(self.frame_2)
        self.table_currentCoinList.setGeometry(QtCore.QRect(0,485,376,560))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
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
        self.table_currentCoinList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table_currentCoinList.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.table_currentCoinList.setAutoScrollMargin(16)
        self.table_currentCoinList.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.table_currentCoinList.setAlternatingRowColors(True)
        self.table_currentCoinList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_currentCoinList.setRowCount(30)
        self.table_currentCoinList.setColumnCount(5)
        self.table_currentCoinList.setObjectName("table_currentCoinList")
        item = QtWidgets.QTableWidgetItem()
        self.table_currentCoinList.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_currentCoinList.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_currentCoinList.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_currentCoinList.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
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
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 140, 1079))
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

        # self.setCentralWidget(self.centralwidget)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def selectedComboItem(self):
        a = self.comboBox1.currentIndex()
        self.webEngineView.setUrl(QtCore.QUrl("https://upbit.com/full_chart?code=CRIX.UPBIT."+json_data[a]["unit_currency"]+"-"+json_data[a]["currency"]))

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
        self.pushButton.setText(_translate("MainWindow", "일"))
        self.pushButton_1.setText(_translate("MainWindow", "주"))
        self.pushButton_2.setText(_translate("MainWindow", "월"))
        self.pushButton_3.setText(_translate("MainWindow", "년"))
        self.pushButton_4.setText(_translate("MainWindow", "테스트"))
        self.pushButton_5.setText(_translate("MainWindow", "10%"))
        self.pushButton_6.setText(_translate("MainWindow", "20%"))
        self.pushButton_7.setText(_translate("MainWindow", "50%"))
        self.pushButton_8.setText(_translate("MainWindow", "100%"))
        self.pushButton_9.setText(_translate("MainWindow", "직접입력"))
        self.pushButton_10.setText(_translate("MainWindow", "자동매매"))
        self.pushButton_11.setText(_translate("MainWindow", "종료하기"))
        self.label_114.setText(_translate("MainWindow", "주문가능"))
        self.label_115.setText(_translate("MainWindow", money_text))
        self.label_116.setText(_translate("MainWindow", "주문총액(KRW)"))
        self.label_117.setText(_translate("MainWindow", "자동 매매 거래 내역"))
        self.back_trading.setText(_translate("MainWindow", "과거 데이터 테스트"))
        self._yield.setText(_translate("MainWindow", "수익률 : 0%"))

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())

    def showModal(self):
        return super().exec_()


# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     win = QtWidgets.QMainWindow()
#     win = Ui_Auto()
#     win.show()
#     sys.exit(app.exec_())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Ui_Auto()
    win.setWindowTitle('HYCOIN')
    win.showMaximized()
    win.show()
    sys.exit(app.exec_())