from PyQt5 import QtCore, QtGui, QtWidgets
# from myPageUi import Ui_MyPage
import cx_Oracle
from PyQt5.QtWidgets import QMessageBox, QComboBox
from PyQt5.QtCore import *
import sys

Connect = cx_Oracle.connect("hycoin/hycoin1234@hycoin.crmeanf0td5o.ap-northeast-2.rds.amazonaws.com:1521/HYCOIN")
Cursor = Connect.cursor()


class Ui_SignUp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setObjectName("Dialog")
        self.resize(1920, 1080)
        self.frameGeometry().center()
        self.setStyleSheet("background-color: rgb(218, 227, 243);")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(220, 30, 201, 51))
        self.label.setObjectName("label")

        # 이름 입력
        self.input_name = QtWidgets.QLineEdit(self)
        self.input_name.setGeometry(QtCore.QRect(300, 120, 151, 31))
        self.input_name.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-color: rgb(170, 85, 255);")
        self.input_name.setObjectName("input_name")

        # 이메일 입력
        self.input_email = QtWidgets.QLineEdit(self)
        self.input_email.setGeometry(QtCore.QRect(300, 160, 151, 31))
        self.input_email.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.input_email.setObjectName("input_email")

        # 아이디 입력
        self.input_id = QtWidgets.QLineEdit(self)
        self.input_id.setGeometry(QtCore.QRect(300, 200, 151, 31))
        self.input_id.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.input_id.setObjectName("input_id")

        # 비밀번호 입력
        self.input_pw = QtWidgets.QLineEdit(self)
        self.input_pw.setGeometry(QtCore.QRect(300, 240, 151, 31))
        self.input_pw.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.input_pw.setObjectName("input_pw")

        # API key 입력
        self.input_api_key = QtWidgets.QLineEdit(self)
        self.input_api_key.setGeometry(QtCore.QRect(300, 320, 151, 31))
        self.input_api_key.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.input_api_key.setObjectName("input_api_key")

        # API Secret Key 입력
        self.input_api_secret = QtWidgets.QLineEdit(self)
        self.input_api_secret.setGeometry(QtCore.QRect(300, 360, 151, 31))
        self.input_api_secret.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.input_api_secret.setObjectName("input_api_secret")

        # text
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(170, 130, 121, 31))
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(170, 360, 121, 31))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(170, 320, 121, 31))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setGeometry(QtCore.QRect(170, 280, 121, 31))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self)
        self.label_7.setGeometry(QtCore.QRect(170, 240, 121, 31))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self)
        self.label_8.setGeometry(QtCore.QRect(170, 210, 121, 31))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self)
        self.label_9.setGeometry(QtCore.QRect(170, 170, 121, 31))
        self.label_9.setObjectName("label_9")

        # 회원가입 버튼
        self.button_signup = QtWidgets.QPushButton(self)
        self.button_signup.setGeometry(QtCore.QRect(290, 410, 101, 41))
        self.button_signup.setStyleSheet("\n"
                                         "background-color: rgb(74, 107, 200);")
        self.button_signup.setObjectName("button_signup")

        # 중복확인 버튼
        self.button_check = QtWidgets.QPushButton(self)
        self.button_check.setGeometry(QtCore.QRect(470, 200, 81, 31))
        self.button_check.setStyleSheet("\n"
                                        "background-color: rgb(74, 107, 200);")
        self.button_check.setObjectName("button_check")

        # market 입력
        self.input_market = QComboBox(self)
        self.input_market.setGeometry(QtCore.QRect(300, 280, 151, 31))
        self.input_market.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.input_market.setObjectName("input_market")
        #
        # self.input_market.setEditable(True)
        # self.input_market.lineEdit().setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.input_market.addItem("---market---")
        self.input_market.addItem("UPBIT")

        self.retranslateUi(self)

        self.button_signup.clicked.connect(self.button_signUp_event)
        self.button_check.clicked.connect(self.button_checkID_event)

        # QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog",
                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; color:#000000;\">Sign Up</span></p></body></html>"))
        self.label_2.setText(_translate("Dialog",
                                        "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; color:#000000;\">이름</span></p></body></html>"))
        self.label_4.setText(_translate("Dialog",
                                        "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; color:#000000;\">API Secret Key</span></p></body></html>"))
        self.label_5.setText(_translate("Dialog",
                                        "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; color:#000000;\">API Key</span></p></body></html>"))
        self.label_6.setText(_translate("Dialog",
                                        "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; color:#000000;\">이용사 선택</span></p></body></html>"))
        self.label_7.setText(_translate("Dialog",
                                        "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; color:#000000;\">비밀번호</span></p></body></html>"))
        self.label_8.setText(_translate("Dialog",
                                        "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; color:#000000;\">아이디</span></p></body></html>"))
        self.label_9.setText(_translate("Dialog",
                                        "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; color:#000000;\">이메일</span></p></body></html>"))
        self.button_signup.setText(_translate("Dialog", "Sign Up"))
        self.button_check.setText(_translate("Dialog", "중복확인"))

    def button_checkID_event(self):
        id = self.input_id.text()
        sql = "select user_name from USER_DB where user_id='{}'".format(id)
        Cursor.execute(sql)
        Connect.commit()
        result = Cursor.fetchall()
        print("result : ", result)
        cnt = Cursor.rowcount
        print("cnt : ", cnt)
        if (cnt > 0):
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Message")
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("이미 존재하는 아이디입니다.")
            msgBox.exec_()
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Message")
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("사용 가능한 아이디입니다.")
            msgBox.exec_()

    def button_signUp_event(self):
        id = self.input_id.text()
        sql = "select user_name from USER_DB where user_id='{}'".format(id)
        Cursor.execute(sql)
        Connect.commit()
        result = Cursor.fetchall()
        cnt = Cursor.rowcount
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Message")
        msgBox.setIcon(QMessageBox.Information)

        if (self.input_name.text() == ""):
            msgBox.setText("이름을 입력해주세요.")
            msgBox.exec_()

        elif (self.input_email.text() == ""):
            msgBox.setText("이메일을 입력해주세요.")
            msgBox.exec_()

        elif (self.input_id.text() == ""):
            msgBox.setText("아이디를 입력해주세요.")
            msgBox.exec_()

        elif (self.input_pw.text() == ""):
            msgBox.setText("비밀번호를 입력해주세요.")
            msgBox.exec_()

        elif (self.input_api_key.text() == ""):
            msgBox.setText("API Key를 입력해주세요.")
            msgBox.exec_()

        elif (self.input_api_secret.text() == ""):
            msgBox.setText("API Secret Key를 입력해주세요.")
            msgBox.exec_()

        elif (cnt > 0):
            msgBox.setText("아이디 중복확인을 해주세요.")
            msgBox.exec_()

        elif (self.input_market.currentIndex() == 0):
            msgBox.setText("이용사를 선택해주세요.")
            msgBox.exec_()

        else:
            name = self.input_name.text()
            email = self.input_email.text()
            id = self.input_id.text()
            pw = self.input_pw.text()
            api_key = self.input_api_key.text()
            secret_key = self.input_api_secret.text()
            market = self.input_market.currentText()
            sql = "insert into USER_DB values('{}','{}','{}','{}','{}','{}','{}')".format(name, email, id, pw, market,
                                                                                          api_key, secret_key)
            Cursor.execute(sql)
            Connect.commit()
            msgBox.setText("회원가입이 완료되었습니다.")
            msgBox.exec_()
            print("bye")
            self.close()
            # close 함수
            # home.widget.show()
            # MainWindow.show()
            # QtCore.QCoreApplication.instance().quit()
            # signUp.close()
            # print(home.widget.currentIndex())

            # widget.setCurrentIndex(widget.currentIndex() - 2)

    def showModal(self):
        return super().exec_()