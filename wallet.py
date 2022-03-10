import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

# 내 계좌 상태
def call_myWallet(acc_key, sec_key):
    access_key = acc_key
    secret_key = sec_key
    server_url = 'https://api.upbit.com/v1/status/wallet'

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url, headers=headers)

    return res.json()

