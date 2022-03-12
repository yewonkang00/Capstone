import requests

# 현재가 정보
def call_price(market):
    url = "https://api.upbit.com/v1/ticker"

    headers = {"Accept": "application/json"}

    query = {'markets':market}

    response = requests.request("GET", url, headers=headers, params=query)

    return response.json()
