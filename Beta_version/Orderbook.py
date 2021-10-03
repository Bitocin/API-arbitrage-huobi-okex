from requests import get

url = 'https://api.hbdm.com/market/depth'
Kilo = {'symbol': 'FIL210924','type': 'step0'}
url2='https://www.okex.com/api/futures/v3/instruments/FIL-USD-210924/book?size=1'



def sell_stock():
    r2 = get(url2)
    r = get(url, params=Kilo)
    s_h = r.json()['tick']['bids'][0][0]/float(r2.json()["asks"][0][0])-1
    s_o = float(r2.json()["bids"][0][0])/r.json()['tick']['asks'][0][0]-1
    avr = (r.json()['tick']['bids'][0][0] + float(r2.json()["asks"][0][0]) +
    float(r2.json()["bids"][0][0]) + r.json()['tick']['asks'][0][0])/4
    return s_o, s_h, avr

