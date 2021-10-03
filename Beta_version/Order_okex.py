import Api_keys
import json
import hmac
import base64
import requests


def okex(params):
    server_time = requests.get('https://www.okex.com/api/general/v3/time')
    timestamp = json.loads(server_time.text)['iso']
    base_url = 'https://www.okex.com'
    request_path = '/api/futures/v3/order'
    url = base_url + request_path
    message = str(timestamp) + 'POST' + request_path + str(json.dumps(params))
    mac = hmac.new(bytes(Api_keys.okex_secret, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    header = dict()
    header['Content-Type'] = 'application/json'
    header['OK-ACCESS-KEY'] = Api_keys.okex_key
    header['OK-ACCESS-SIGN'] = base64.b64encode(d)
    header['OK-ACCESS-TIMESTAMP'] = str(timestamp)
    header['OK-ACCESS-PASSPHRASE'] = Api_keys.Passphrase
    body = json.dumps(params)
    print(requests.post(url, data=body, headers=header).json())