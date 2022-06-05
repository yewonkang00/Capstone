import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests


def call_accounts(acc_key, sec_key):


    server_url = 'https://api.upbit.com/v1/accounts'

    payload = {
        'access_key': acc_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, sec_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url, headers=headers)

    print(res.json())
    return res.json()
