from PyQt5 import QtCore, QtGui, QtWidgets
from myPageUi import Ui_MyPage
import cx_Oracle
from PyQt5.QtWidgets import QMessageBox, QComboBox
import sys

Connect = cx_Oracle.connect("hycoin/hycoin1234@hycoin.crmeanf0td5o.ap-northeast-2.rds.amazonaws.com:1521/HYCOIN")
Cursor = Connect.cursor()

class Ui_MainDialog(object):

    def setupUI(self, MainDialog):
        MainDialog.setObjectName("MainDialog")
        MainDialog.resize(1920, 1080)
        MainDialog.setStyleSheet("background-color: rgb(218, 227, 243);")

        self.button_signin = QtWidgets.QPushButton(MainDialog)
        self.button_signin.setGeometry(QtCore.QRect(870, 490, 180, 50)) #sign in 위치, 크기
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
        self.button_signin.clicked.connect(self.button_signin_event)    # 로그인 버튼


        self.button_signup = QtWidgets.QPushButton(MainDialog)
        self.button_signup.setGeometry(QtCore.QRect(870, 560, 180, 50)) #sign up 위치, 크기
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
        self.button_signup.clicked.connect(self.button_signup_event) # 회원가입 버튼

        self.lineEdit_id = QtWidgets.QLineEdit(MainDialog)
        self.lineEdit_id.setGeometry(QtCore.QRect(835, 350, 250, 45)) #username or email 위치, 크기
        self.lineEdit_id.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_id.setPlaceholderText(" Username or email address")
        self.lineEdit_id.setObjectName("lineEdit_id")


        self.lineEdit_pw = QtWidgets.QLineEdit(MainDialog)
        self.lineEdit_pw.setGeometry(QtCore.QRect(835, 410, 250, 45)) #password 위치, 크기
        self.lineEdit_pw.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_pw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_pw.setPlaceholderText(" Password")
        self.lineEdit_pw.setObjectName("lineEdit_pw")


        self.label = QtWidgets.QLabel(MainDialog)
        self.label.setGeometry(QtCore.QRect(860, 250, 200, 50)) #sign in 텍스트
        self.label.setObjectName("label")




        self.retranslateUi(MainDialog)
        QtCore.QMetaObject.connectSlotsByName(MainDialog)


    def button_signin_event(self):
        input_id = self.lineEdit_id.text()
        input_pw = self.lineEdit_pw.text()

        sql = "select user_pw from USER_DB where user_id = '{}'".format(input_id)

        print("sql : " + sql)
        Cursor.execute(sql)

        result = Cursor.fetchall()
        print("result : ", result)
        cnt = Cursor.rowcount
        print("cnt : ", cnt)

        print("test : ", cnt == 0)

        msgBox = QMessageBox()
        msgBox.setWindowTitle("Message")
        msgBox.setIcon(QMessageBox.Information)

        if(cnt == 0) :
            msgBox.setText("존재하지 않는 아이디입니다.")
            msgBox.exec_()

        else :
            pw = result[0][0]
            print("pw : ", pw)
            if(pw == input_pw) :
                widget.setCurrentIndex(widget.currentIndex()+1)

            else :
                msgBox.setText("비밀번호가 잘못 입력 되었습니다.")
                msgBox.exec_()


    def button_signup_event(self):
        widget.setCurrentIndex(widget.currentIndex()+2)

    def retranslateUi(self, MainDialog):
        _translate = QtCore.QCoreApplication.translate
        MainDialog.setWindowTitle(_translate("MainDialog", "Dialog"))
        self.button_signin.setText(_translate("MainDialog", "Sign in"))
        self.button_signup.setText(_translate("MainDialog", "Sign up"))
        self.label.setText(_translate("MainDialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; color:#000000;\">SIGN IN</span></p></body></html>"))


class Ui_SignUp(object):

    def setupUI(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1920, 1080)
        Dialog.frameGeometry().center()
        Dialog.setStyleSheet("background-color: rgb(218, 227, 243);")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(220, 30, 201, 51))
        self.label.setObjectName("label")

        # 이름 입력
        self.input_name = QtWidgets.QLineEdit(Dialog)
        self.input_name.setGeometry(QtCore.QRect(300, 120, 151, 31))
        self.input_name.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-color: rgb(170, 85, 255);")
        self.input_name.setObjectName("input_name")

        # 이메일 입력
        self.input_email = QtWidgets.QLineEdit(Dialog)
        self.input_email.setGeometry(QtCore.QRect(300, 160, 151, 31))
        self.input_email.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.input_email.setObjectName("input_email")

        # 아이디 입력
        self.input_id = QtWidgets.QLineEdit(Dialog)
        self.input_id.setGeometry(QtCore.QRect(300, 200, 151, 31))
        self.input_id.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.input_id.setObjectName("input_id")

        # 비밀번호 입력
        self.input_pw = QtWidgets.QLineEdit(Dialog)
        self.input_pw.setGeometry(QtCore.QRect(300, 240, 151, 31))
        self.input_pw.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.input_pw.setObjectName("input_pw")

        # API key 입력
        self.input_api_key = QtWidgets.QLineEdit(Dialog)
        self.input_api_key.setGeometry(QtCore.QRect(300, 320, 151, 31))
        self.input_api_key.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.input_api_key.setObjectName("input_api_key")

        # API Secret Key 입력
        self.input_api_secret = QtWidgets.QLineEdit(Dialog)
        self.input_api_secret.setGeometry(QtCore.QRect(300, 360, 151, 31))
        self.input_api_secret.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.input_api_secret.setObjectName("input_api_secret")

        # text
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(170, 130, 121, 31))
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(170, 360, 121, 31))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(170, 320, 121, 31))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(170, 280, 121, 31))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(170, 240, 121, 31))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(170, 210, 121, 31))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(170, 170, 121, 31))
        self.label_9.setObjectName("label_9")

        # 회원가입 버튼
        self.button_signup = QtWidgets.QPushButton(Dialog)
        self.button_signup.setGeometry(QtCore.QRect(290, 410, 101, 41))
        self.button_signup.setStyleSheet("\n"
                                         "background-color: rgb(74, 107, 200);")
        self.button_signup.setObjectName("button_signup")

        # 중복확인 버튼
        self.button_check = QtWidgets.QPushButton(Dialog)
        self.button_check.setGeometry(QtCore.QRect(470, 200, 81, 31))
        self.button_check.setStyleSheet("\n"
                                        "background-color: rgb(74, 107, 200);")
        self.button_check.setObjectName("button_check")

        # market 입력
        self.input_market = QComboBox(Dialog)
        self.input_market.setGeometry(QtCore.QRect(300, 280, 151, 31))
        self.input_market.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.input_market.setObjectName("input_market")
        self.input_market.addItem("---market---")
        self.input_market.addItem("UPBIT")

        self.retranslateUi(Dialog)

        self.button_signup.clicked.connect(self.button_signUp_event)


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

    def button_signUp_event(self):
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
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Message")
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("회원가입이 완료되었습니다.")
        msgBox.exec_()
        widget.setCurrentIndex(widget.currentIndex()-2)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # 화면 전환용 widget
    widget = QtWidgets.QStackedWidget()
    # 로그인 widget
    MainWindow = QtWidgets.QDialog()
    ui = Ui_MainDialog()
    ui.setupUI(MainWindow)
    widget.addWidget(MainWindow)

    # 마이페이지 widget
    myPage = QtWidgets.QMainWindow()
    ui2 = Ui_MyPage()
    ui2.setupUI(myPage)
    widget.addWidget(myPage)

    # 회원가입 widget
    signUp = QtWidgets.QDialog()
    ui3 = Ui_SignUp()
    ui3.setupUI(signUp)
    widget.addWidget(signUp)

    widget.show()
    app.exec_()