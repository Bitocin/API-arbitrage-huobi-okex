# # development phase
# import ast
# import base64
# import hashlib
# import hmac
# import json
# import requests
# import threading
# import time
# import websocket
# import zlib
# import ssl
# import traceback
#
# # wss://api.huobi.pro/ws
#
# from urllib import parse
# from datetime import datetime
#
# def json_replace(msg):
#     msg = msg.replace('true', 'True').replace('false', 'False').replace('null', 'None')
#     return msg
#
#
# class BaseClient(object):
#     def __init__(self, **kwargs):
#         self._api_key = kwargs.get('api_key')
#         self._secret_key = kwargs.get('secret_key')
#         self._socket = None
#         self._thread = None
#         self._state = False
#         self._request = []
#
#     @property
#     def state(self):
#         return self._state
#
#     def start(self):
#         raise NotImplementedError
#
#     def on_open(self):
#         raise NotImplementedError
#
#     def on_close(self):
#         self._state = False
#
#     def on_error(self, errs):
#         print(errs)
#
#     def on_message(self, msg):
#         raise NotImplementedError
#
#
# class HuobiWebSocket(BaseClient):
#     def __init__(self, **kwargs):
#         super(HuobiWebSocket, self).__init__(**kwargs)
#         self._wss_url = 'wss://api.huobi.pro/ws/v2'  # 或 wss://api-aws.huobi.pro/ws/v2
#         self._mbp_url = 'wss://api.huobi.pro/feed'  # 或 wss://api-aws.huobi.pro/feed
#         self._client_id = str(time.time())
#         self._socket_mbp = None
#
#     def _sign(self):
#         params = {
#             'accessKey': self._api_key,
#             'signatureMethod': 'HmacSHA256',
#             'signatureVersion': '2.1',
#             'timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
#         }
#         target = sorted(params.items(),
#                         key=lambda x: x[0], reverse=False)  # 参数ASCII排序
#         to_sign = '\n'.join(
#             ['GET', 'api.huobi.pro', '/ws/v2', parse.urlencode(target)])
#         params.update({
#             'signature': base64.b64encode(hmac.new(self._secret_key.encode(),
#                             to_sign.encode(), hashlib.sha256).digest()).decode(),
#             'authType': 'api'
#         })
#         auth_params = {
#             "action": "req",
#             'ch': 'auth',
#             'params': params,
#         }
#         return auth_params
#
#     def _subscribe(self, params):
#         self._socket.send(json.dumps(params))
#
#     def _subscribe_mbp(self, params):
#         self._socket_mbp.send(json.dumps(params))
#
#     def bbo(self, symbol):
#         """ 买一卖一逐笔行情 """
#         params = {
#             "sub": f"market.{symbol}.bbo",
#             "id": self._client_id
#         }
#         self._subscribe(params)
#
#     def accounts(self, mode=0):
#         """订阅账户变更
#         mode: 推送方式，有效值：0, 1，默认值：0
#         """
#         params = {
#             "action": "sub",
#             "ch": f"accounts.update#{mode}"
#         }
#         self._subscribe(params)
#
#     def start(self):
#         self._socket = websocket.WebSocketApp(self._wss_url, on_message=self.on_message,
#                     on_open=self.on_open, on_error=self.on_error, on_close=self.on_close)
#         self._socket_mbp = websocket.WebSocketApp(self._mbp_url, on_message=self.on_message,
#                     on_open=self.on_open, on_error=self.on_error, on_close=self.on_close)
#         self._thread = threading.Thread(target=self._ws.run_forever, kwargs={"sslopt": {"cert_reqs": ssl.CERT_NONE}})
#         self._thread.start()
#
#     def on_open(self):
#         self._state = True
#         # 选择是否设置签名
#         self._socket.send(json.dumps(self._sign()))
#         # 订阅行情数据
#         raise NotImplementedError
#
#     def on_message(self, msg):
#         try:
#             msg = json_replace(msg)
#             rsp = ast.literal_eval(msg)
#             if rsp.get('action') == 'ping':
#                 self._ws.send(json.dumps({"action": "pong", "data": {"ts":rsp["data"]["ts"]}}))
#             elif rsp.get('action') == 'req' and rsp.get('code') == 200:
#                 # 订阅资产及订单
#                 raise NotImplementedError
#             else:
#                 # 处理接收数据
#                 raise NotImplementedError
#         except Exception as e:
#             raise NotImplementedError