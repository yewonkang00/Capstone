# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/temp/tradingUi.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1366, 768)
        MainWindow.setInputMethodHints(QtCore.Qt.ImhNone)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: rgb(255,255,255)")

        # 검색창
        self.edit_search = QtWidgets.QLineEdit(self.centralwidget)
        self.edit_search.setGeometry(QtCore.QRect(190, 40, 480, 35))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.edit_search.setFont(font)
        self.edit_search.setObjectName("edit_search")

        # 검색창 돋보기 이미지
        self.image_search = QtWidgets.QGraphicsView(self.centralwidget)
        self.image_search.setGeometry(QtCore.QRect(145, 40, 35, 35))
        self.image_search.setStyleSheet("border-image: url(resources/search.png); background-repeat: no-repeat;")
        self.image_search.setObjectName("image_search")

        # 왼쪽 프레임
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 80, 981, 1021))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.setStyleSheet("background-color:none;")

        # 코인이미지
        self.image_coin = QtWidgets.QGraphicsView(self.frame)
        self.image_coin.setGeometry(QtCore.QRect(150, 17, 35, 35))
        self.image_coin.setStyleSheet("border-image: url(resources/bitcoin.png); background-repeat: no-repeat;")
        self.image_coin.setObjectName("image_coin")

        # 코인명(예.비트코인)
        self.label_coinName = QtWidgets.QLabel(self.frame)
        self.label_coinName.setGeometry(QtCore.QRect(190, 10, 200, 50))
        self.label_coinName.setObjectName("label_coinName")
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_coinName.setFont(font)


        # 코인명 옆에 회색으로 알파벳 코드(예.BTC)
        self.label_coinNickname = QtWidgets.QLabel(self.frame)
        self.label_coinNickname.setGeometry(QtCore.QRect(300, 3, 150, 70))
        self.label_coinNickname.setObjectName("label_coinNickname")
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        self.label_coinNickname.setFont(font)
        self.label_coinNickname.setStyleSheet("color: GREY;")

        # 호가 레이블
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(190, 40, 150, 70))
        self.label_3.setObjectName("label_3")
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_3.setFont(font)


        # 호가 테이블
        self.tableWidget = QtWidgets.QTableWidget(self.frame)
        self.tableWidget.setGeometry(QtCore.QRect(190, 100, 480, 534))
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
        self.button_cancel_1.setGeometry(QtCore.QRect(190, 599, 91, 35))
        self.button_cancel_1.setObjectName("button_cancel_1")
        self.button_cancel_1.setStyleSheet("border: 1px solid grey; background-color:white; color: blue;")

        # 테이블 헤더: 파란색 매물
        self.label_40 = QtWidgets.QLabel(self.frame)
        self.label_40.setGeometry(QtCore.QRect(280, 599, 91, 35))
        self.label_40.setObjectName("label_40")
        self.label_40.setStyleSheet("border: 1px solid grey; background-color:white;")
        self.label_40.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        # 테이블 헤더: 수량
        self.button_quantity = QtWidgets.QPushButton(self.frame)
        self.button_quantity.setGeometry(QtCore.QRect(370, 599, 91, 35))
        self.button_quantity.setObjectName("button_quantity")
        self.button_quantity.setStyleSheet("border: 1px solid grey; background-color:white;")

        # 테이블 헤더: 빨간색 매물
        self.label_41 = QtWidgets.QLabel(self.frame)
        self.label_41.setGeometry(QtCore.QRect(460, 599, 91, 35))
        self.label_41.setObjectName("label_41")
        self.label_41.setStyleSheet("border: 1px solid grey; background-color:white;")
        self.label_41.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


        # 테이블 헤더: 일괄취소(빨간색)
        self.button_cancel_2 = QtWidgets.QPushButton(self.frame)
        self.button_cancel_2.setGeometry(QtCore.QRect(550, 599, 91, 35))
        self.button_cancel_2.setObjectName("button_cancel_2")
        self.button_cancel_2.setStyleSheet("border: 1px solid grey; background-color:white; color: red;")

        # 오른쪽 프레임
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setStyleSheet("background-color:none;")
        self.frame_2.setGeometry(QtCore.QRect(700, 0, 683, 768))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")


        # 보유종목
        self.comboBox = QtWidgets.QComboBox(self.frame_2)
        self.comboBox.setGeometry(QtCore.QRect(60, 40, 200, 35))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("보유종목")
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.comboBox.setFont(font)



        # 종목정보 Frame
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setStyleSheet("background-color:none;")
        self.frame_3.setGeometry(QtCore.QRect(20, 70, 941, 391))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")

        # 거래량
        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setGeometry(QtCore.QRect(40, 40, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # 거래량 Number
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        self.label_4.setGeometry(QtCore.QRect(70, 40, 150, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")

        # 거래량 BTC
        self.label_5 = QtWidgets.QLabel(self.frame_3)
        self.label_5.setGeometry(QtCore.QRect(160, 40, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")


        # 거래대금
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        self.label_2.setGeometry(QtCore.QRect(40, 60, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        # 거래대금 Number
        self.label_6 = QtWidgets.QLabel(self.frame_3)
        self.label_6.setGeometry(QtCore.QRect(60, 60, 150, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")

        # 거래대금 백만원
        self.label_7 = QtWidgets.QLabel(self.frame_3)
        self.label_7.setGeometry(QtCore.QRect(165, 60, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")

        # 최근24시간
        self.label_8 = QtWidgets.QLabel(self.frame_3)
        self.label_8.setGeometry(QtCore.QRect(115, 80, 150, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")

        # 구분선
        self.line = QtWidgets.QFrame(self.frame_3)
        self.line.setGeometry(QtCore.QRect(40, 100, 381, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # 52주최고
        self.label_9 = QtWidgets.QLabel(self.frame_3)
        self.label_9.setGeometry(QtCore.QRect(40, 120, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")

        # 52주최고 Number
        self.label_10 = QtWidgets.QLabel(self.frame_3)
        self.label_10.setGeometry(QtCore.QRect(115, 120, 150, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("color: RED;")
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")

        # 52주최고 Date
        self.label_11 = QtWidgets.QLabel(self.frame_3)
        self.label_11.setGeometry(QtCore.QRect(115, 140, 150, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")

        # 52주최저
        self.label_14 = QtWidgets.QLabel(self.frame_3)
        self.label_14.setGeometry(QtCore.QRect(40, 170, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")

        # 52주최저 Number
        self.label_12 = QtWidgets.QLabel(self.frame_3)
        self.label_12.setGeometry(QtCore.QRect(115, 170, 150, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("color: BLUE;")
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")

        # 52주최저 Date
        self.label_13 = QtWidgets.QLabel(self.frame_3)
        self.label_13.setGeometry(QtCore.QRect(115, 190, 150, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")

        # 전일종가
        self.label_16 = QtWidgets.QLabel(self.frame_3)
        self.label_16.setGeometry(QtCore.QRect(325, 120, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")

        #전일종가 Number
        self.label_15 = QtWidgets.QLabel(self.frame_3)
        self.label_15.setGeometry(QtCore.QRect(400, 120, 150, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("")
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")

        # 당일고가
        self.label_19 = QtWidgets.QLabel(self.frame_3)
        self.label_19.setGeometry(QtCore.QRect(325, 140, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")

        # 당일고가 Number
        self.label_17 = QtWidgets.QLabel(self.frame_3)
        self.label_17.setGeometry(QtCore.QRect(400, 140, 150, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_17.setFont(font)
        self.label_17.setStyleSheet("color: RED;")
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")

        # 당일최고등락률
        self.label_18 = QtWidgets.QLabel(self.frame_3)
        self.label_18.setGeometry(QtCore.QRect(400, 165, 150, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_18.setFont(font)
        self.label_18.setStyleSheet("color: RED;")
        self.label_18.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_18.setObjectName("label_18")

        # 당일저가
        self.label_22 = QtWidgets.QLabel(self.frame_3)
        self.label_22.setGeometry(QtCore.QRect(325, 190, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")

        # 당일저가 Number
        self.label_20 = QtWidgets.QLabel(self.frame_3)
        self.label_20.setGeometry(QtCore.QRect(400, 190, 150, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_20.setFont(font)
        self.label_20.setStyleSheet("color: BLUE;")
        self.label_20.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")

        # 당일최저등락률
        self.label_21 = QtWidgets.QLabel(self.frame_3)
        self.label_21.setGeometry(QtCore.QRect(400, 215, 150, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_21.setFont(font)
        self.label_21.setStyleSheet("color: BLUE;")
        self.label_21.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_21.setObjectName("label_21")

        # 매수버튼
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setGeometry(QtCore.QRect(60, 320, 175, 60))
        self.pushButton.setObjectName("pushButton")

        # 매도버튼
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_2.setGeometry(QtCore.QRect(230, 320, 175, 60))
        self.pushButton_2.setObjectName("pushButton_2")

        #거래내역
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_3.setGeometry(QtCore.QRect(400, 320, 175, 60))
        self.pushButton_3.setObjectName("pushButton_3")

        # 매수매도거래내역 프레임
        self.frame_order = QtWidgets.QFrame(self.frame_2)
        self.frame_order.setGeometry(QtCore.QRect(60, 375, 515, 350))
        self.frame_order.setStyleSheet("background-color:grey;")
        self.frame_order.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_order.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_order.setObjectName("frame_order")

        # 왼쪽 메뉴 프레임
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 100, 768))
        self.frame.setStyleSheet("background-color: rgb(50, 90, 160)")  # 배경색 설정
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # 메뉴-마이페이지 버튼
        self.menuButton_myPage_3 = QtWidgets.QPushButton(self.frame)
        self.menuButton_myPage_3.setGeometry(QtCore.QRect(21, 50, 60, 60))
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
        self.menuButton_trading_3.setGeometry(QtCore.QRect(21, 150, 60, 60))
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
        self.menuButton_chart_3.setGeometry(QtCore.QRect(21, 250, 60, 60))
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
        self.menuButton_autoTrading_3.setGeometry(QtCore.QRect(21, 350, 60, 60))
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
        self.menuButton_setting_3.setGeometry(QtCore.QRect(21, 450, 60, 60))
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
        self.menuButton_exit_3.setGeometry(QtCore.QRect(21, 650, 60, 60))
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
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
