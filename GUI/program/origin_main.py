from PyQt5 import QtCore, QtGui, QtWidgets
import cx_Oracle
from PyQt5.QtWidgets import QMessageBox, QComboBox
from PyQt5.QtCore import *
import sys
import origin_module

Connect = cx_Oracle.connect("hycoin/hycoin1234@hycoin.crmeanf0td5o.ap-northeast-2.rds.amazonaws.com:1521/HYCOIN")
Cursor = Connect.cursor()

class Ui_MainDialog(QtWidgets.QDialog):

    user_id = ""

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setObjectName("MainDialog")
        self.resize(1920, 1080)
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

        user_id = "abc"
        # self.set_id()
        print("user_id:", user_id)

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
                # send_instance_signal = pyqtSignal("PyQt_PyObject")
                # self.send_instance_signal.connect(self)
                # widget.setCurrentIndex(widget.currentIndex()+1)
                # self.display()
                # self.show()

                # self.user_signal.emit(input_id)

                # win = origin_mypage.Ui_MyPage()
                # r = win.showModal()
                win = origin_module.Ui_MyPage()
                r = win.showModal()
                # self.closeEvent()


            else :
                msgBox.setText("비밀번호가 잘못 입력 되었습니다.")
                msgBox.exec_()

    # def button_signup_event(self):
    #     win = origin_signup.Ui_SignUp()
    #     r = win.showModal()

    # @pyqtSlot(str)
    # def user_slot(self, arg1):
    #     print(arg1)

    def set_id(self):
        global user_id
        user_id = self.lineEdit_id.text()

    def retranslateUi(self, MainDialog):
        _translate = QtCore.QCoreApplication.translate
        MainDialog.setWindowTitle(_translate("MainDialog", "Dialog"))
        self.button_signin.setText(_translate("MainDialog", "Sign in"))
        self.button_signup.setText(_translate("MainDialog", "Sign up"))
        self.label.setText(_translate("MainDialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; color:#000000;\">SIGN IN</span></p></body></html>"))

    # def display_signup(self):
    #     self.w = origin_signup.Ui_SignUp()

    def closeEvent(self, event):
        self.close()

    def show(self):
        super().show()

    # def get_id(self):
    #     user_id = self.lineEdit_id.text()
    #     print("user_id:", user_id)

# app = QtWidgets.QApplication(sys.argv)
# window = Ui_MainDialog()
# window.show()
# sys.exit(app.exec())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Ui_MainDialog()
    win.show()
    sys.exit(app.exec_())