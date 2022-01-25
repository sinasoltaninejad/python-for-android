# import kivy module
import kivy
from kivy.clock import Clock
kivy.require("1.9.1")
from kivy.app import App
import ccxt
import pandas as pd
import talib
from datetime import datetime



kucoin_api = '61eaf1e11d12c200015e9d4b'
kucoin_sec = 'f111db50-46a9-4f4a-b11d-1dc603c27ef6'
kucoin_pass = '123456789'

kucoin = ccxt.kucoinfutures({
    'apiKey': kucoin_api,
    'secret': kucoin_sec,
    'password': kucoin_pass,
    'option': {'defaultMarket': 'futures'}
})


pos = False
price_buy=0
sell = 0
buy = 0
amount = 1
pnl=0
posi = []
leverage = 3
symbol = 'ADA/USDT:USDT'
kivy.require('1.11.1')


def c(self):
    global pos
    global price_buy
    try:

        tim = int(kucoin.fetch_time()/1000)
        t = datetime.fromtimestamp(tim)
        if pos == True:
            price_last = kucoin.fetch_ticker(symbol)
            price_last = price_last['last']
            pnl = (price_last - price_buy)/price_buy * 100 * leverage

            if pnl < -0.75:
                price_sell = kucoin.fetch_ticker(symbol)
                price_sell = price_sell['last']
                kucoin.create_market_sell_order(symbol, amount, params={'closeOrder': True})

                print('sell', price_sell, t)
                pos = False

            if pnl > 2.5:
                price_sell = kucoin.fetch_ticker(symbol)
                price_sell = price_sell['last']
                kucoin.create_market_sell_order(symbol, amount,  params={'closeOrder': True})

                print('sell', price_sell,t)
                pos = False



        if t.minute % 5 == 0 and t.second == 1:
            print(t.hour,t.minute,t.second)
            ohlcv = kucoin.fetch_ohlcv(symbol=symbol, timeframe='5m', since=None, limit=100)
            df = pd.DataFrame(ohlcv, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            ema3 = talib.EMA(df['Close'], 3)
            ema9 = talib.EMA(df['Close'], 9)

            if pos == False:

                if (ema3[97] <= ema9[97] and ema3[98] > ema9[98]):
                    price_buy = kucoin.fetch_ticker(symbol)
                    price_buy = price_buy['last']
                    order_buy = kucoin.create_market_buy_order(symbol, amount,
                                                              {'leverage': leverage})
                    print(order_buy)
                    print('buy', 'price_buy=', price_buy,t)
                    pos = True

            if pos == True:

                if (ema3[97] >= ema9[97] and ema3[98] < ema9[98]):
                    price_sell = kucoin.fetch_ticker(symbol)
                    price_sell = price_sell['last']
                    sell_order=kucoin.create_market_sell_order(symbol, amount,  params={'closeOrder': True})
                    print(sell_order)
                    pnl2 = (price_sell - price_buy) / price_buy * 100 * leverage
                    print('sell', 'price_sell=', price_sell,t)
                    pos = False


    except ccxt.BaseError as Error:
        print('error', Error)






 class MyFirstKivyApp(App):

    # Function that returns
    # the root widget
    def build(self):
        # Label with text Hello World is
        # returned as root widget
        Clock.schedule_interval(c, 1)
        return Label(text="Hello World !")

    # Here our class is initialized


# and its run() method is called.
# This initializes and starts
# our Kivy application.
MyFirstKivyApp().run()
