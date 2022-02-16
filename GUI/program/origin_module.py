from origin_mypage import Ui_MyPage
from origin_signup import Ui_SignUp

class event(object):
    def button_signup_event(self):
        win = Ui_SignUp()
        r = win.showModal()

    # def button_mypage_event(self):
    #     win = Ui_MyPage()
    #     r = win.showModal()
