import requests
import time
import datetime as dt

def get_day_candle(coin_name, time, n):
    # 기준일-1 부터 n일까지의 일봉 요청
    time = dt.datetime(time.year, time.month, time.day, 0, 0, 0)
    url = "https://api.upbit.com/v1/candles/days"
    headers = {"Accept": "application/json"}
    querystring = {"market": coin_name,
                   "count": n,
                   "to": time
                   }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()


def get_30min_candle(coin_name, time):
    time = dt.datetime(time.year, time.month, time.day, 0, 0, 0) + dt.timedelta(days=1)
    url = "https://api.upbit.com/v1/candles/minutes/30"
    headers = {"Accept": "application/json"}
    querystring = {"market": coin_name,
                   "count": 48,
                   "to": time
                   }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()


def score_moving_average(coin_day_candle, n):
    # k일 이평선의 n일 이평선 스코어
    k = 5
    response = coin_day_candle
    score = 0
    for i in range(n):
        temp = 0
        for j in range(k):
            temp += response[i + j + 1]["trade_price"]
        if response[i]["high_price"] > temp / k:
            score += 1
    return score / n


def compute_k(coin_day_candle):
    # utc 최근 20일간의 noise ratio 평균
    response = coin_day_candle
    k = 0
    for i in response:
        k += 1 - abs(i["opening_price"] - i["trade_price"]) / (i["high_price"] - i["low_price"])
    return k / 20


def compute_range(coin_day_candle):
    # 전날 (고가) - (저가)
    return coin_day_candle[0]['high_price'] - coin_day_candle[0]['low_price']


# main
start_day = dt.datetime(2018, 3, 1, 0, 0, 0)
end_day = dt.datetime(2019, 4, 1, 0, 0, 0)
t = start_day
coin_name = 'KRW-BTC'
my_money = 1
p_cnt = 0
k_cnt = 0
while t < end_day:
    day_candle = get_day_candle(coin_name, t, 30)
    min_candle = get_30min_candle(coin_name, t)

    scma = score_moving_average(day_candle, 18)
    c_k = compute_k(day_candle)
    rng = compute_range(day_candle)
    target_price = min_candle[-1]['opening_price'] + c_k * rng
    sell_price = 0
    chk = 0
    chk_trade = 0
    loss_cut_chk = 0
    # 만약 30분봉 종가가 목표가 이상이면, 거래
    # if min_candle[-1]['candle_date_time_utc'].split('T')[1] == '00:00:00':
    for j in range(47, -1, -1):
        if chk == 0 and min_candle[j]['trade_price'] >= target_price:
            chk = 1
            p_cnt += 1
        if chk == 1 and chk_trade == 0 and (min_candle[j]['low_price'] < target_price < min_candle[j]['high_price']):
            chk_trade = 1
            k_cnt += 1
            print('구매시간대 :',min_candle[j]['candle_date_time_utc'], '목표가 :', target_price, end=' ')

        if chk_trade == 1 and min_candle[j]['trade_price'] < target_price*0.98:
            loss_cut_chk = 1
            sell_price = min_candle[j]['trade_price']
            print('손절가 :', sell_price)
            break
    if chk_trade == 1:
        if loss_cut_chk == 0:
            sell_price = min_candle[0]['trade_price']
        real_yield = (sell_price/target_price*0.999-1)*scma + 1
        Ryield = (sell_price/target_price-1)*scma*10 + 1
        my_money *= Ryield
        print('당일 종가 :',min_candle[0]['trade_price'], '수익률 :',real_yield, '레버리지 수익률 :', Ryield, '잔고 :', my_money, 'scma : ', scma)
    t += dt.timedelta(days=1)
    time.sleep(1/20)

print(my_money, p_cnt, k_cnt)
