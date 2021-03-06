import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import jwt
import uuid
import requests
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import cx_Oracle
import origin_module

Connect = cx_Oracle.connect("hycoin/hycoin1234@hycoin.crmeanf0td5o.ap-northeast-2.rds.amazonaws.com:1521/HYCOIN")
Cursor = Connect.cursor()

access_key = 'aaa'
secret_key = 'aaa'
server_url = 'https://api.upbit.com'

user_id = ""


price_arr = []  # 코인 평가 금액 배열

class Ui_MyPage(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        global access_key, secret_key
        access_key = origin_module.access_key
        secret_key = origin_module.secret_key

        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
        }
        jwt_token = jwt.encode(payload, secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        # 코인 목록
        res = requests.get(server_url + "/v1/accounts", headers=headers)
        json_data = res.json()
        print("json_data: ", json_data)
        # if(json_data['error']['message'] == '인증된 IP가 아닙니다.'):
        # if(json_data == "{'error': {'message': '인증된 IP가 아닙니다.', 'name': 'no_authorization_i_p'}}"):
        #     msgBox = QMessageBox()
        #     msgBox.setWindowTitle("Message")
        #     msgBox.setIcon(QMessageBox.Information)
        #     msgBox.setText("인증된 IP가 아닙니다.")
        #     msgBox.exec_()
        #     self.close()
        self.total = 0
        global price_arr
        url = "https://api.upbit.com/v1/candles/minutes/1?count=1&market="
        for i in json_data:
            print(i)
            if i["currency"] != "KRW":
                headers2 = {"Accept": "application/json"}
                response = requests.request("GET", str(url + i["unit_currency"] + "-" + i["currency"]),
                                            headers=headers2)
                data = response.json()
                # print(response.text)
                # print("test: ", data[0]["trade_price"])
                a = int(float(data[0]["trade_price"]) * float(i["balance"]))
                price_arr.append(a)
                self.total += a

            else:
                self.total += int(float(i["balance"]))

            # print("total : ", total)
            print(i["currency"])

        self.total_text = ""  # 총 평가금액
        self.coin_total_text = ""
        self.money_text = ""
        self.avg_buy_text = ""
        self.total_text = str(self.total) + " 원"  # 총 평가금액
        # print('total_text', total_text)
        coin_total = self.total - int(float(json_data[0]["balance"]))

        self.coin_total_text = str(coin_total) + " 원"  # 코인 총 평가금액
        # print('coin_total_text', coin_total_text)
        # 주문 가능 금액
        money = int(float(json_data[0]["balance"]))
        print(money)
        self.money_text = str(money) + " 원"

        # 매수 평균가
        avg_buy = int(float(json_data[0]["avg_buy_price"]))
        print(avg_buy)
        self.avg_buy_text = str(avg_buy) + " 원"

        self.setObjectName("MainWindow")
        self.setFixedSize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        # 전체프레임
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.frame_2.setMouseTracking(True)
        self.frame_2.setAutoFillBackground(False)
        self.frame_2.setStyleSheet("background-color: rgb(255,255,255)")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setMidLineWidth(0)
        self.frame_2.setObjectName("frame_2")

        # 파이 그래프
        self.series = QPieSeries()
        cnt = 0
        for i in json_data:
            if(i["currency"] == "KRW") :
                self.series.append("KRW", round((((float(i["balance"])/self.total))*100)))

            else :
                a = price_arr[cnt]
                cnt += 1
                self.series.append(i["currency"], round((((a/self.total)*100))))
                print("percent: ", int((a/self.total)*100))

        # self.series.append("BTC", 80)
        # self.series.append("ETH", 70)
        # self.series.append("XRP", 50)
        # self.series.append("DOGE", 40)
        # self.series.append("KRW", 30)

        # adding slice
        self.slice = QPieSlice()
        self.slice = self.series.slices()[cnt]
        self.slice.setExploded(True)
        self.slice.setLabelVisible(True)
        # self.slice.setPen(QPen(Qt.blue, 2))
        self.slice.setBrush(Qt.blue)

        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        self.chartview = QChartView(self.chart)
        self.chartview.setRenderHint(QPainter.Antialiasing)

        # 파이그래표 위치/크기
        self.pie_chart = QtWidgets.QFrame(self.frame_2)
        self.pie_chart.setGeometry(QtCore.QRect(177, 98, 843, 492))
        self.pie_chart.setObjectName("pieChart")
        # self.pie_chart.setStyleSheet("background-color:none;")
        self.pie_chart_layout = QHBoxLayout()
        self.pie_chart_layout.addWidget(self.chartview)
        self.pie_chart.setLayout(self.pie_chart_layout)

        # # 코인별 비율 표시
        # self.frame_ratio = QLabel(self)
        # self.frame_ratio.move(100,100)
        # self.frame_ratio.setText("hello")
        
        # 총 평가금액 프레임
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setGeometry(QtCore.QRect(411, 56, 351, 112))
        self.frame_3.setStyleSheet(
            """
            border: 2px solid #F0F;
            border-width: 3;
            border-color: rgb(50, 90, 160);
            border-radius: 20%;
            """
        )
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")

        # 총 평가금액 내용
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame_3)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(105, 20, 141, 84))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_totalMoneyTitle = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_totalMoneyTitle.sizePolicy().hasHeightForWidth())
        self.label_totalMoneyTitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(14)
        self.label_totalMoneyTitle.setFont(font)
        self.label_totalMoneyTitle.setStyleSheet("border:none;")
        self.label_totalMoneyTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.label_totalMoneyTitle.setObjectName("label_totalMoneyTitle")
        self.verticalLayout.addWidget(self.label_totalMoneyTitle)
        self.label_totalMoney = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.label_totalMoney.sizePolicy().hasHeightForWidth())
        self.label_totalMoney.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        # font.setBold(True)
        font.setPointSize(18)
        self.label_totalMoney.setFont(font)
        self.label_totalMoney.setStyleSheet("border: none; border-radius: 0%; padding-top: 10;")
        self.label_totalMoney.setAlignment(QtCore.Qt.AlignCenter)
        self.label_totalMoney.setObjectName("label_totalMoney")
        self.verticalLayout.addWidget(self.label_totalMoney)

        # 코인 보유현황 제목
        self.label_currentCoinListTitle = QtWidgets.QLabel(self.frame_2)
        self.label_currentCoinListTitle.setGeometry(QtCore.QRect(411, 570, 150, 70))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_currentCoinListTitle.setFont(font)
        self.label_currentCoinListTitle.setObjectName("label_currentCoinListTitle")

        # 코인 보유 현황 리스트
        self.table_currentCoinList = QtWidgets.QTableWidget(self.frame_2)
        self.table_currentCoinList.setGeometry(QtCore.QRect(411, 640, 1200, 320))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_currentCoinList.sizePolicy().hasHeightForWidth())
        self.table_currentCoinList.setSizePolicy(sizePolicy)
        self.table_currentCoinList.setMouseTracking(False)
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.table_currentCoinList.horizontalHeader().setFont(font)
        self.table_currentCoinList.setFont(font)
        self.table_currentCoinList.setStyleSheet(
            """
            QHeaderView::section {
                background-color:#404040;
                border: 0px;
                color:#FFFFFF;
            }
            
            QTableView {
                border: 0px;
            }
            """
        )

        self.table_currentCoinList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table_currentCoinList.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.table_currentCoinList.setAutoScrollMargin(16)
        self.table_currentCoinList.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.table_currentCoinList.setAlternatingRowColors(True)
        self.table_currentCoinList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_currentCoinList.setRowCount(cnt)
        self.table_currentCoinList.setColumnCount(8)
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
        item = QtWidgets.QTableWidgetItem()
        self.table_currentCoinList.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_currentCoinList.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_currentCoinList.setHorizontalHeaderItem(7, item)
        self.table_currentCoinList.horizontalHeader().setVisible(True)
        self.table_currentCoinList.horizontalHeader().setFixedHeight(45)
        self.table_currentCoinList.horizontalHeader().setDefaultSectionSize(147)  # 테이블 기본 열 크기
        self.table_currentCoinList.horizontalHeader().setSortIndicatorShown(True)
        self.table_currentCoinList.horizontalHeader().setStretchLastSection(False)
        self.table_currentCoinList.verticalHeader().setVisible(False)  # 행 번호 안보이게 설정
        self.table_currentCoinList.verticalHeader().setCascadingSectionResizes(False)
        self.table_currentCoinList.verticalHeader().setDefaultSectionSize(40)  # 테이블 기본 행 크기
        self.table_currentCoinList.verticalHeader().setHighlightSections(True)
        self.table_currentCoinList.setSelectionMode(QAbstractItemView.NoSelection)  # 선택 불능
        self.table_currentCoinList.setEditTriggers(QAbstractItemView.NoEditTriggers)  # edit 금지 모드
        self.table_currentCoinList.setShowGrid(False)  # grid line 숨기기

        ###################
        count = 0
        for i in json_data:
            print('json_data',json_data)
            if (i["currency"] == "KRW"): pass
            else:
                buy_data = int(float(i["balance"]) * float(i["avg_buy_price"]))
                print(i["currency"])
                res = requests.request("GET", "https://api.upbit.com/v1/ticker?markets=KRW-" + str(i["currency"]), headers={"Accept": "application/json"})
                data = res.json()
                print(data)

                now_price = int(float(data[0]["trade_price"]) * float(i["balance"]))
                self.table_currentCoinList.setItem(count, 0, QTableWidgetItem(str(i["currency"])))  # 보유코인
                self.table_currentCoinList.item(count, 0).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                print('e1')
                self.table_currentCoinList.setItem(count, 1, QTableWidgetItem(str(now_price - buy_data)))  # 평가손익
                self.table_currentCoinList.item(count, 1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                print('e2')
                # print(data[0]["trade_price"], int(i["avg_buy_price"]) - 1) 여기 문제
                print(buy_data, now_price)
                self.table_currentCoinList.setItem(count, 2, QTableWidgetItem(str((round((now_price / buy_data-1)*100, 2)))+ '%')) # 수익률
                self.table_currentCoinList.item(count, 2).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                print('e3')

                self.table_currentCoinList.setItem(count, 3, QTableWidgetItem(str(i["balance"])))  # 보유수량
                self.table_currentCoinList.item(count, 3).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                print('e4')

                self.table_currentCoinList.setItem(count, 4, QTableWidgetItem(str(now_price)))  # 평가금액
                self.table_currentCoinList.item(count, 4).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                print('e5')

                self.table_currentCoinList.setItem(count, 5, QTableWidgetItem(str(i["avg_buy_price"])))  # 매수평균가
                self.table_currentCoinList.item(count, 5).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                print('e6')

                self.table_currentCoinList.setItem(count, 6, QTableWidgetItem(str(int(data[0]["trade_price"]))))  # 현재가
                self.table_currentCoinList.item(count, 6).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                print('e7')

                self.table_currentCoinList.setItem(count, 7, QTableWidgetItem(str(buy_data)))  # 매수금액
                self.table_currentCoinList.item(count, 7).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                count += 1
                print('end')
        
        # 주문가능금액 프레임
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setGeometry(QtCore.QRect(1050, 281, 514, 204))
        self.frame_4.setStyleSheet("background-color: #B5C7ED;")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")

        # 주문가능금액 밑의 메뉴 프레임
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.frame_4)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 514, 204))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_availableMoneyTitle = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_availableMoneyTitle.sizePolicy().hasHeightForWidth())
        self.label_availableMoneyTitle.setSizePolicy(sizePolicy)
        self.label_availableMoneyTitle.setMinimumSize(QtCore.QSize(0, 0))
        self.label_availableMoneyTitle.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(15)
        self.label_availableMoneyTitle.setFont(font)
        self.label_availableMoneyTitle.setStyleSheet("margin-top:10; margin-left:10;")
        self.label_availableMoneyTitle.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_availableMoneyTitle.setObjectName("label_availableMoneyTitle")
        self.verticalLayout_3.addWidget(self.label_availableMoneyTitle)
        self.label_availableMoney = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_availableMoney.sizePolicy().hasHeightForWidth())
        self.label_availableMoney.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("LG Smart UI Bold")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_availableMoney.setFont(font)
        self.label_availableMoney.setAlignment(QtCore.Qt.AlignCenter)
        self.label_availableMoney.setObjectName("label_availableMoney")
        self.verticalLayout_3.addWidget(self.label_availableMoney)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_charging = QtWidgets.QPushButton(self.verticalLayoutWidget_3)

        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(13)
        self.button_charging.setFont(font)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_charging.sizePolicy().hasHeightForWidth())

        # 충전
        self.button_charging.setSizePolicy(sizePolicy)
        self.button_charging.setMinimumSize(QtCore.QSize(0, 35))
        self.button_charging.setObjectName("button_charging")
        self.horizontalLayout_2.addWidget(self.button_charging)
        self.button_sending = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_sending.sizePolicy().hasHeightForWidth())

        # 출금
        self.button_sending.setSizePolicy(sizePolicy)
        self.button_sending.setObjectName("button_sending")
        self.horizontalLayout_2.addWidget(self.button_sending)
        self.button_bankingHistory = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(13)
        self.button_sending.setFont(font)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_bankingHistory.sizePolicy().hasHeightForWidth())

        # 입출금내역
        self.button_bankingHistory.setSizePolicy(sizePolicy)
        self.button_bankingHistory.setObjectName("button_bankingHistory")
        self.horizontalLayout_2.addWidget(self.button_bankingHistory)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(13)
        self.button_bankingHistory.setFont(font)

        # 코인 프레임
        self.frame_5 = QtWidgets.QFrame(self.frame_2)
        self.frame_5.setGeometry(QtCore.QRect(1050, 56, 514, 204))
        self.frame_5.setStyleSheet("background-color: #B6D1D4;")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")

        # 코인 금액 프레임
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.frame_5)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 514, 204))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_currentCoinTitle = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_currentCoinTitle.sizePolicy().hasHeightForWidth())
        self.label_currentCoinTitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(15)
        self.label_currentCoinTitle.setFont(font)
        self.label_currentCoinTitle.setStyleSheet("margin-left: 10; margin-top: 10;")
        self.label_currentCoinTitle.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_currentCoinTitle.setObjectName("label_currentCoinTitle")
        self.verticalLayout_2.addWidget(self.label_currentCoinTitle)
        self.label_currentCoin = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_currentCoin.sizePolicy().hasHeightForWidth())
        self.label_currentCoin.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("LG Smart UI Bold")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_currentCoin.setFont(font)
        self.label_currentCoin.setAlignment(QtCore.Qt.AlignCenter)
        self.label_currentCoin.setObjectName("label_currentCoin")
        self.verticalLayout_2.addWidget(self.label_currentCoin)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # 보유코인 버튼
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 35))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(13)
        self.pushButton.setFont(font)

        # 거래내역 버튼
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(13)
        self.pushButton_2.setFont(font)

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

        # self.setCentralWidget(self.centralwidget)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def button_trade_event(self):
        origin_module.trade_check = 1
        self.close()
        win = origin_module.Ui_Trading()
        r = win.showModal()
        #self.close()

    def button_chart_event(self):
        origin_module.chart_check = 1
        self.close()
        win = origin_module.Ui_Chart()
        r = win.showModal()
        #self.close()

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
        #self.close()

    def button_mypage_event(self):
        self.close()
        win = origin_module.Ui_MyPage()
        # self.close()
        r = win.showModal()
        #self.close()

    def button_close_event(self):
        self.close()

    def button_setup_event(self):
        self.close()
        win = origin_module.Ui_Setup()
        r = win.showModal()
        #self.close()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MyPage"))
        self.table_currentCoinList.setSortingEnabled(True)
        item = self.table_currentCoinList.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "보유코인"))
        item = self.table_currentCoinList.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "평가손익"))
        item = self.table_currentCoinList.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "수익률"))
        item = self.table_currentCoinList.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "보유수량"))
        item = self.table_currentCoinList.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "평가금액"))
        item = self.table_currentCoinList.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "매수평균가"))
        item = self.table_currentCoinList.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "현재가"))
        item = self.table_currentCoinList.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "매수금액"))
        self.label_currentCoinListTitle.setText(_translate("MainWindow", "보유현황"))
        self.label_totalMoneyTitle.setText(_translate("MainWindow", "총 평가금액"))
        self.label_totalMoney.setText(_translate("MainWindow",self.total_text))
        self.label_availableMoneyTitle.setText(_translate("MainWindow", "주문가능금액"))
        self.label_availableMoney.setText(_translate("MainWindow", self.money_text))
        self.button_charging.setText(_translate("MainWindow", "충전"))
        self.button_sending.setText(_translate("MainWindow", "출금"))
        self.button_bankingHistory.setText(_translate("MainWindow", "입출금내역"))
        self.label_currentCoinTitle.setText(_translate("MainWindow", "코인"))
        self.label_currentCoin.setText(_translate("MainWindow", self.coin_total_text))
        self.pushButton.setText(_translate("MainWindow", "보유 코인"))
        self.pushButton_2.setText(_translate("MainWindow", "거래내역"))

    def showModal(self):
        return super().exec_()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Ui_MyPage()
    win.setWindowTitle('HYCOIN')
    #win.showMaximized()
    win.show()
    sys.exit(app.exec_())