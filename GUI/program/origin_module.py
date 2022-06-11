from origin_signup import Ui_SignUp
from origin_tradingUi import Ui_Trading
from origin_chart import Ui_Chart
from origin_mypage import Ui_MyPage
from origin_setup import Ui_Setup
import origin_mypage
from origin_predict import Ui_Predict
from origin_auto import Ui_Auto

class event(object):
    def button_signup_event(self):
        win = Ui_SignUp()

        r = win.showModal()

user_id = 'aaa'
user_pw = 'aaa'
access_key = 'aaa'
secret_key = 'aaa'
user_email = 'aaa'
chart_check = 1
trade_check = 1
predict_check = 1

def set_id(temp_id):
    global user_id
    user_id = temp_id

def set_pw(temp_pw):
    global user_pw
    user_pw = temp_pw

def set_email(temp_email):
    global user_email
    user_email = temp_email

def set_info(access, secret):
    global access_key, secret_key
    access_key = access
    secret_key = secret