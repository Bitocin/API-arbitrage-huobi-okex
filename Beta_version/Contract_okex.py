import Api_keys
import json
import hmac
import base64
import requests

def contract_okex():
    request_path = '/api/futures/v3/FIL-USD-210924/position'
    base_url = 'https://www.okex.com'
    server_time = requests.get('https://www.okex.com/api/general/v3/time')
    timestamp = json.loads(server_time.text)['iso']

    message = str(timestamp) + 'GET' + request_path
    mac = hmac.new(bytes(Api_keys.okex_secret, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    header = dict()
    header['OK-ACCESS-KEY'] = Api_keys.okex_key
    header['OK-ACCESS-SIGN'] = base64.b64encode(d)
    header['OK-ACCESS-TIMESTAMP'] = str(timestamp)
    header['OK-ACCESS-PASSPHRASE'] = Api_keys.Passphrase
    response = requests.get(base_url + request_path, headers=header)

    a = float(response.json()["holding"][-1]["long_qty"])
    if a > 0:
        o = "l"
    elif float(response.json()["holding"][-1]["short_qty"]) > 0:
        o = "s"
    else:
        o = "n"
    return o