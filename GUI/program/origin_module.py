from origin_signup import Ui_SignUp
from origin_tradingUi import Ui_Trading
from origin_chart import Ui_Chart
from origin_mypage import Ui_MyPage
import origin_mypage
from origin_auto import Ui_Auto

class event(object):
    def button_signup_event(self):
        win = Ui_SignUp()

        r = win.showModal()

    # def button_trade_event(self):
    #     win = Ui_Trading()
    #     #self.close()
    #     r = win.showModal()
    #
    # def button_chart_event(self):
    #     win = Ui_Chart()
    #     #self.close()
    #     r = win.showModal()
    #
    # def button_mypage_event(self):
    #     win = Ui_MyPage()
    #     #self.close()
    #     r = win.showModal()
    #
    # def button_close_event(self):
    #     self.close()

user_id = 'aaa'
access_key = 'aaa'
secret_key = 'aaa'

def set_id(temp_id):
    global user_id
    user_id = temp_id

def set_info(access, secret):
    global access_key, secret_key
    access_key = access
    secret_key = secret