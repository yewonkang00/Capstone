import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

def trade_coin(access_k, secret_k, coin_name, side, volume, price, ord_type):
    #주문 종류, 주문량, 주문 가격 코인 거래
    #매도는 주문량, 매수는 가격
    server_url = "https://api.upbit.com/v1/orders"
    if ord_type == 'limit': #지정가 주문
        query = {
            'market': coin_name,
            'side': side,
            'volume': volume,
            'price': price,
            'ord_type': ord_type,
        }
    elif ord_type == 'price': #시장가 매수
        query = {
            'market': coin_name,
            'side': side,
            'price': price,
            'ord_type': ord_type,
        }
    else : #시장가 매도
        query = {
            'market': coin_name,
            'side': side,
            'volume': volume,
            'ord_type': ord_type,
        }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url, params=query, headers=headers)
    return res.json()

