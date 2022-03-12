import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

def call_orders(acc_key, sec_key, state, uuid_param):

    access_key = acc_key
    secret_key = sec_key
    server_url = 'https://api.upbit.com/v1/orders'

    query = {
        'state': state,
    }
    query_string = urlencode(query)

    uuids = [
        uuid_param,
        # ...
    ]
    uuids_query_string = '&'.join(["uuids[]={}".format(uuid) for uuid in uuids])

    query['uuids[]'] = uuids
    query_string = "{0}&{1}".format(query_string, uuids_query_string).encode()

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

    res = requests.get(server_url, params=query, headers=headers)

    print(res.json())
    return res.json()

