import Api_keys
import requests
import base64
import hashlib
import urllib
import datetime
import hmac
import json

def leverge_huobi():
    def createSign(pParams, method, host_url, request_path, secret_key):
        sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
        encode_params = urllib.parse.urlencode(sorted_params)
        payload = [method, host_url, request_path, encode_params]
        payload = '\n'.join(payload)
        payload = payload.encode(encoding='UTF8')
        secret_key = secret_key.encode(encoding='UTF8')

        digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest)
        signature = signature.decode()
        return signature

    params = { 'symbol': 'fil'}
    request_path = "/api/v1/contract_account_info"
    method = 'POST'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params_to_sign = {'AccessKeyId': Api_keys.huobi_key,
                      'SignatureMethod': 'HmacSHA256',
                      'SignatureVersion': '2',
                      'Timestamp': timestamp}
    host_url = 'https://api.hbdm.com'
    host_name = urllib.parse.urlparse(host_url).hostname
    params_to_sign['Signature'] = createSign(params_to_sign, method, host_name, request_path, Api_keys.huobi_secret)
    url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
    headers = {
                "Accept": "application/json",
                'Content-Type': 'application/json'
            }
    postdata = json.dumps(params)
    response = requests.post(url, postdata, headers=headers, timeout=10)
    margin_position = response.json()["data"][-1]["margin_position"]
    margin_balance = response.json()["data"][-1]["margin_balance"]
    r_h = (margin_balance/(margin_position+0.00000001))/10
    return r_h
