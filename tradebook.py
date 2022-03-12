import requests

# 최근 거래내역(특정 계좌 거래내역 아님)
def call_trade_book(market, last_trade_record_time, count, cursor, daysAgo):
    url = "https://api.upbit.com/v1/trades/ticks?count=1"

    headers = {"Accept": "application/json"}

    query = {
        'market': market,  # 마켓 코드 (ex. KRW-BTC)
        'to': last_trade_record_time,  # 마지막 체결 시각. 형식 : [HHmmss 또는 HH:mm:ss]. 비워서 요청시 가장 최근 데이터
        'count': count,  # 체결 개수
        'cursor': cursor,  # 페이지네이션 커서 (sequentialId)
        'daysAgo': daysAgo  # 최근 체결 날짜 기준 7일 이내의 이전 데이터 조회 가능. 비워서 요청 시 가장 최근 체결 날짜 반환. (범위: 1 ~ 7))
    }

    response = requests.request("GET", url, headers=headers, params=query)

    return response.json()
