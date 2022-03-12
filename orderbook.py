import requests

# 호가창 정보
def call_orderBook(coinName):
    url = "https://api.upbit.com/v1/orderbook"

    headers = {"Accept": "application/json"
               }

    query = {
        'markets': coinName
    }

    response = requests.request("GET", url, headers=headers, params=query)

    # print(response.text)
    return response.json()

