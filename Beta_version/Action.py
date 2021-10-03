from Leverage_okex import leverge_okex
from Leverage_huobi import leverge_huobi
from Contract_okex import contract_okex
from Contract_huobi import contract_huobi
from Orderbook import sell_stock
from Order_huobi import huobi
from Order_okex import okex

open_short_huobi = {'contract_code': 'fil210924', 'volume': '1', 'offset': 'open', 'lever_rate': '10', 'direction': 'sell', 'order_price_type': 'opponent'}
open_long_huobi = {'contract_code': 'fil210924', 'volume': '1', 'offset': 'open', 'lever_rate': '10', 'direction': 'buy', 'order_price_type': 'opponent'}
close_short_huobi = {'contract_code': 'fil210924', 'volume': '1', 'offset': 'close', 'lever_rate': '10', 'direction': 'buy', 'order_price_type': 'opponent'}
close_long_huobi = {'contract_code': 'fil210924', 'volume': '1', 'offset': 'close', 'lever_rate': '10', 'direction': 'sell', 'order_price_type': 'opponent'}
open_long_okex = {'type': '1', 'size': '1', 'order_type': '4', 'instrument_id': 'FIL-USD-210924'}
open_short_okex = {'type': '2', 'size': '1', 'order_type': '4', 'instrument_id': 'FIL-USD-210924'}
close_long_okex = {'type': '3', 'size': '1', 'order_type': '4', 'instrument_id': 'FIL-USD-210924'}
close_short_okex = {'type': '4', 'size': '1', 'order_type': '4', 'instrument_id': 'FIL-USD-210924'}

while True:
    a = 0
    h = contract_huobi()
    o = contract_okex()
    r_h = leverge_huobi()
    r_o = leverge_okex()
    if r_h > r_o:
        r = r_o
    else:
        r = r_h
    s_o, s_h, avr = sell_stock()
    const = avr

    while 0.995*const < avr < 1.005*const:
        s_o = s_o - 0.005
        s_h = s_h + 0.005
        if r > 0.2:
            if s_o*100 > 1/256/r**3 + 0.4:
                if h == "l":
                    huobi(open_long_huobi)
                    okex(open_short_okex)
                elif o == "l":
                    huobi(close_short_huobi)
                    okex(close_long_okex)
                else:
                    if h == "n":
                        huobi(open_long_huobi)
                    else:
                        huobi(close_short_huobi)
                    okex(open_short_okex)
                print("1")
                break
            elif s_h*100 > 1/256/r**3 + 0.4:
                if o == "l":
                    huobi(open_short_huobi)
                    okex(open_long_okex)
                elif h == "l":
                    huobi(close_long_huobi)
                    okex(close_short_okex)
                else:
                    huobi(open_short_huobi)
                    if o == "n":
                        okex(open_long_okex)
                    else:
                        okex(close_short_okex)
                print("2")
                break

        if r_h < r_o:
            if h == "s":
                if s_o*-100 < 1/r_h**4/2048 - r_h/2:
                    huobi(close_short_huobi)
                    if o == "l":
                        okex(close_long_okex)
                    else:
                        okex(open_short_okex)
                    print("3")
                    break

            if h == "l" or h == "n":
                if s_h*-100 < 1/r_h**4/2048 - r_h/2:
                    if h == "n":
                        huobi(open_short_huobi)
                    else:
                        huobi(close_long_huobi)
                    okex(close_short_okex)
                    print("4")
                    break
        else:
            if o == "s":
                if s_h*-100 < 1/r_o**4/2048 - r_o/2:
                    if h == "l":
                        huobi(close_long_huobi)
                    else:
                        huobi(open_short_huobi)
                    okex(close_short_okex)
                    print("5")
                    break

            if o == "l" or o == "n":
                if s_o*-100 < 1/r_o**4/2048 - r_o/2:
                    huobi(close_short_huobi)
                    if o == "n":
                        okex(open_short_okex)
                    else:
                        okex(close_long_okex)
                    print("6")
                    break
        s_o, s_h, avr = sell_stock()
    print("Sell na Huobi: " + str(s_h))
    print("Sell na Okex: " + str(s_o))
    print("Huobi: " + str(1/r_h))
    print("Okex: " + str(1/r_o))

