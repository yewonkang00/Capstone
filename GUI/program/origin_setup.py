import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import origin_module
import cx_Oracle
from PyQt5.QtWidgets import QMessageBox

Connect = cx_Oracle.connect("hycoin/hycoin1234@hycoin.crmeanf0td5o.ap-northeast-2.rds.amazonaws.com:1521/HYCOIN")
Cursor = Connect.cursor()

class Ui_Setup(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        user_id = origin_module.user_id
        self.setObjectName("MainWindow")
        self.resize(1920, 1080)
        self.setInputMethodHints(QtCore.Qt.ImhNone)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: rgb(255,255,255)")

        # 중앙프레임
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setStyleSheet("background-color:none;")
        self.frame_2.setGeometry(QtCore.QRect(200, 100, 1720, 920))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        # 이름 텍스트
        self.label_Name = QtWidgets.QLabel(self.frame_2)
        self.label_Name.setGeometry(QtCore.QRect(320, 10, 281, 70))
        self.label_Name.setObjectName("label_Name")
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.label_Name.setFont(font)

        # 비밀번호변경 텍스트
        self.label_change = QtWidgets.QLabel(self.frame_2)
        self.label_change.setGeometry(QtCore.QRect(307, 150, 281, 70))
        self.label_change.setObjectName("label_change")
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.label_change.setFont(font)

        # 현재비밀번호 텍스트
        self.current_password = QtWidgets.QLabel(self.frame_2)
        self.current_password.setGeometry(QtCore.QRect(372, 200, 211, 98))
        self.current_password.setObjectName("current_password")
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.current_password.setFont(font)
        self.current_password.setStyleSheet("color: GREY;")

        # 현재 비밀번호 입력창
        self.input_current_password = QtWidgets.QLineEdit(self.frame_2)
        self.input_current_password.setGeometry(QtCore.QRect(600, 220, 500, 49))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.input_current_password.setFont(font)
        self.input_current_password.setObjectName("input_current_password")

        # 새 비밀번호 텍스트
        self.new_password = QtWidgets.QLabel(self.frame_2)
        self.new_password.setGeometry(QtCore.QRect(372, 300, 211, 98))
        self.new_password.setObjectName("new_password")
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.new_password.setFont(font)
        self.new_password.setStyleSheet("color: GREY;")

        # 새 비밀번호 입력창
        self.input_new_password = QtWidgets.QLineEdit(self.frame_2)
        self.input_new_password.setGeometry(QtCore.QRect(600, 320, 500, 49))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.input_new_password.setFont(font)
        self.input_new_password.setObjectName("input_new_password")

        # 새 비밀번호 확인 텍스트
        self.new_password2 = QtWidgets.QLabel(self.frame_2)
        self.new_password2.setGeometry(QtCore.QRect(372, 400, 211, 98))
        self.new_password2.setObjectName("new_password2")
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.new_password2.setFont(font)
        self.new_password2.setStyleSheet("color: GREY;")

        # 새 비밀번호 확인 입력창
        self.input_new_password2 = QtWidgets.QLineEdit(self.frame_2)
        self.input_new_password2.setGeometry(QtCore.QRect(600, 420, 500, 49))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.input_new_password2.setFont(font)
        self.input_new_password2.setObjectName("input_new_password2")

        # 변경하기 버튼
        self.pushButton_1 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_1.setGeometry(QtCore.QRect(600, 500, 154, 45))
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_1.clicked.connect(self.button_pwChange_event)

        # 알림 설정 텍스트
        self.notification  = QtWidgets.QLabel(self.frame_2)
        self.notification.setGeometry(QtCore.QRect(307, 570, 281, 70))
        self.notification.setObjectName("notification")
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.notification.setFont(font)

        # 알림 설정 버튼
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_2.setGeometry(QtCore.QRect(600, 580, 154, 45))
        self.pushButton_2.setObjectName("pushButton_1")

        # 회원탈퇴 텍스트
        self.withdraw = QtWidgets.QLabel(self.frame_2)
        self.withdraw.setGeometry(QtCore.QRect(307, 640, 281, 70))
        self.withdraw.setObjectName("withdraw ")
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.withdraw.setFont(font)

        # 회원탈퇴 버튼
        self.pushButton_3= QtWidgets.QPushButton(self.frame_2)
        self.pushButton_3.setGeometry(QtCore.QRect(600, 650, 154, 45))
        self.pushButton_3.setObjectName("pushButton_1")
        self.pushButton_3.clicked.connect(self.button_deleteID_event)

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

        #         self.setCentralWidget(self.centralwidget)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        # def button_myPage_event(self):
        #     widget.setCurrentIndex(widget.currentIndex() + 1)

    def button_trade_event(self):
        origin_module.trade_check = 1
        self.close()
        win = origin_module.Ui_Trading()
        r = win.showModal()
        # self.close()

    def button_chart_event(self):
        origin_module.chart_check = 1
        self.close()
        win = origin_module.Ui_Chart()
        r = win.showModal()
        # self.close()

    def button_auto_event(self):
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
        self.close()
        win = origin_module.Ui_MyPage()
        # self.close()
        r = win.showModal()
        # self.close()

    def button_close_event(self):
        self.close()

    def button_setup_event(self):
        self.close()
        win = origin_module.Ui_Setup()
        r = win.showModal()
        # self.close()

    def button_pwChange_event(self):
        id = origin_module.user_id
        sql = "select user_pw from USER_DB where user_id = '{}'".format(id)
        Cursor.execute(sql)
        result = Cursor.fetchall()
        pw = result[0][0]
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Message")
        msgBox.setIcon(QMessageBox.Information)

        if(pw != self.input_current_password.text()):
            msgBox.setText("현재 비밀번호가 일치하지 않습니다.")
            msgBox.exec_()

        elif(self.input_new_password.text() != self.input_new_password2.text()):
            msgBox.setText("새 비밀번호를 다시 확인해주세요.")
            msgBox.exec_()

        else:
            sql = "update user_db set user_pw ='{}' where user_id='{}'".format(self.input_new_password.text(), id)
            Cursor.execute(sql)
            Connect.commit()
            msgBox.setText("비밀번호가 변경되었습니다.")
            msgBox.exec_()

    def button_deleteID_event(self):
        id = origin_module.user_id
        reply = QMessageBox.question(self, 'Message', '회원 탈퇴하시겠습니까?', QMessageBox.Yes | QMessageBox.No)
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Message")
        msgBox.setIcon(QMessageBox.Information)

        if reply == QMessageBox.Yes:
            sql = "update user_db set valid ='{}' where user_id='{}'".format('0', id)
            Cursor.execute(sql)
            Connect.commit()
            msgBox.setText("회원 탈퇴되었습니다.")
            msgBox.exec_()
            self.close()


        # else:
        #     name = self.input_name.text()
        #     email = self.input_email.text()
        #     id = self.input_id.text()
        #     pw = self.input_pw.text()
        #     api_key = self.input_api_key.text()
        #     secret_key = self.input_api_secret.text()
        #     market = self.input_market.currentText()
        #     sql = "insert into USER_DB values('{}','{}','{}','{}','{}','{}','{}','{}')".format(name, email, id, pw, market,
        #                                                                                   api_key, secret_key, 1)
        #     Cursor.execute(sql)
        #     Connect.commit()
        #     msgBox.setText("회원가입이 완료되었습니다.")
        #     msgBox.exec_()
        #     print("bye")
        #     self.close()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_Name.setText(_translate("MainWindow", "홍길동님"))
        self.label_change.setText(_translate("MainWindow", "비밀번호변경"))
        self.current_password.setText(_translate("MainWindow", "현재 비밀번호"))
        self.new_password.setText(_translate("MainWindow", "새 비밀번호"))
        self.new_password2.setText(_translate("MainWindow", "새 비밀번호 확인"))
        self.notification.setText(_translate("MainWindow", "알림 설정"))
        self.withdraw.setText(_translate("MainWindow", "회원탈퇴"))

        self.pushButton_1.setText(_translate("MainWindow", "변경하기"))
        self.pushButton_2.setText(_translate("MainWindow", "알림해지"))
        self.pushButton_3.setText(_translate("MainWindow", "탈퇴하기"))

    def showModal(self):
        return super().exec_()

#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Ui_Setup()
    win.setWindowTitle('HYCOIN')
    #win.showMaximized()
    win.show()
    sys.exit(app.exec_())