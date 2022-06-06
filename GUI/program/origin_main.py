from PyQt5 import QtCore, QtGui, QtWidgets
import cx_Oracle
from PyQt5.QtWidgets import QMessageBox, QComboBox
from PyQt5.QtCore import *
import sys
import origin_module

Connect = cx_Oracle.connect("hycoin/hycoin1234@hycoin.crmeanf0td5o.ap-northeast-2.rds.amazonaws.com:1521/HYCOIN")
Cursor = Connect.cursor()
secret_key = 'aaa'
access_key = 'aaa'
user_email = 'aaa'

class Ui_MainDialog(QtWidgets.QDialog):
    user_id = ""
    user_pw = ""
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setObjectName("MainDialog")
        self.setFixedSize(1920, 1080)
        self.setStyleSheet("background-color: rgb(218, 227, 243);")

        self.button_signin = QtWidgets.QPushButton(self)
        self.button_signin.setGeometry(QtCore.QRect(870, 490, 180, 50))  # sign in 위치, 크기
        self.button_signin.setStyleSheet("\n"
                                         "background-color: rgb(68, 114, 196);")
        self.button_signin.setObjectName("pushButton")
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.button_signin.setStyleSheet("color: white;"
                                         "background-color: rgb(68, 114, 196);"
                                         "border-style: dashed;"
                                         "border-color: #1E90FF")
        self.button_signin.setFont(font)
        self.button_signin.clicked.connect(self.button_signin_event)  # 로그인 버튼

        self.button_signup = QtWidgets.QPushButton(self)
        self.button_signup.setGeometry(QtCore.QRect(870, 560, 180, 50))  # sign up 위치, 크기
        self.button_signup.setStyleSheet("\n"
                                         "background-color: rgb(68, 114, 196);")
        self.button_signup.setObjectName("button_signup")
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.button_signup.setStyleSheet("color: white;"
                                         "background-color: rgb(68, 114, 196);"
                                         "border-style: dashed;"
                                         "border-color: #1E90FF")
        self.button_signup.setFont(font)
        # self.button_signup.clicked.connect(self.button_signup_event)  # 회원가입 버튼
        self.button_signup.clicked.connect(origin_module.event.button_signup_event)  # 회원가입 버튼

        self.lineEdit_id = QtWidgets.QLineEdit(self)
        self.lineEdit_id.setGeometry(QtCore.QRect(835, 350, 250, 45))  # username or email 위치, 크기
        self.lineEdit_id.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_id.setPlaceholderText(" Username or email address")
        self.lineEdit_id.setObjectName("lineEdit_id")

        self.lineEdit_pw = QtWidgets.QLineEdit(self)
        self.lineEdit_pw.setGeometry(QtCore.QRect(835, 410, 250, 45))  # password 위치, 크기
        self.lineEdit_pw.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_pw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_pw.setPlaceholderText(" Password")
        self.lineEdit_pw.setObjectName("lineEdit_pw")

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(860, 250, 200, 50))  # sign in 텍스트
        self.label.setObjectName("label")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def button_signin_event(self):
        input_id = self.lineEdit_id.text()
        input_pw = self.lineEdit_pw.text()

        global user_id
        user_id = input_id
        print("user_id:", user_id)

        sql = "select user_pw from USER_DB where user_id = '{}'".format(input_id)
        print("sql : " + sql)
        Cursor.execute(sql)

        result = Cursor.fetchall()
        print("result : ", result)
        cnt = Cursor.rowcount
        print("cnt : ", cnt)

        print("test : ", cnt == 0)

        sql2 = "select valid from user_db where user_id = '{}'".format(input_id)
        Cursor.execute(sql2)
        result2 = Cursor.fetchall()
        print("result2 : ", result2)
        valid = result2[0][0]
        print("valid : ", valid)

        msgBox = QMessageBox()
        msgBox.setWindowTitle("Message")
        msgBox.setIcon(QMessageBox.Information)

        if(cnt == 0) :
            msgBox.setText("존재하지 않는 아이디입니다.")
            msgBox.exec_()

        elif(valid == '0') :
            msgBox.setText("탈퇴한 아이디입니다.")
            msgBox.exec_()

        else :
            global user_pw
            user_pw = result[0][0]
            print("pw : ", user_pw)
            if(user_pw == input_pw) :
                sql = "select API_KEY from USER_DB where user_id = '{}'".format(user_id)
                print("sql : " + sql)
                Cursor.execute(sql)
                global access_key
                result = Cursor.fetchall()
                access_key = result[0][0]
                print("access_key : ", access_key)

                sql = "select SECRET_KEY from USER_DB where user_id = '{}'".format(user_id)
                print("sql : " + sql)
                Cursor.execute(sql)
                global secret_key
                result = Cursor.fetchall()
                # print("result :", result)
                secret_key = result[0][0]
                print("secret_key : ", secret_key)

                sql = "select user_email from USER_DB where user_id = '{}'".format(user_id)
                print("sql : " + sql)
                Cursor.execute(sql)
                global user_email
                result = Cursor.fetchall()
                # print("result :", result)
                user_email = result[0][0]
                print("user_email : ", user_email)

                origin_module.set_id(str(user_id))
                origin_module.set_info(access_key, secret_key)
                origin_module.set_pw(str(user_pw))
                origin_module.set_email(str(user_email))

                # print("origin_module id", origin_module.user_id)
                # origin_module.origin_mypage.set_id(str(user_id))
                win = origin_module.Ui_MyPage()
                r = win.showModal()
                self.close()

            else :
                msgBox.setText("비밀번호가 잘못 입력 되었습니다.")
                msgBox.exec_()

    def retranslateUi(self, MainDialog):
        _translate = QtCore.QCoreApplication.translate
        MainDialog.setWindowTitle(_translate("MainDialog", "Dialog"))
        self.button_signin.setText(_translate("MainDialog", "Sign in"))
        self.button_signup.setText(_translate("MainDialog", "Sign up"))
        self.label.setText(_translate("MainDialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; color:#000000;\">SIGN IN</span></p></body></html>"))

    def showModal(self):
        return super().exec_()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Ui_MainDialog()
    win.setWindowTitle('HYCOIN')
    # win.showMaximized()
    win.show()
    sys.exit(app.exec_())