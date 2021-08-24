import json
from pykrx import stock
from datetime import datetime

def get_ohlcv(today):
    df_stock = stock.get_market_ohlcv_by_ticker(date=today,market="ALL")
    df_stock = df_stock.reset_index()
    df_stock.columns = ['code','open','high','low','close','volume','amount','rate']
    js_stock = df_stock.to_json(orient='records',force_ascii=False)
    js_file = open("../data/stock_data.json", "w", encoding='utf-8')
    json.dump(js_stock,js_file,ensure_ascii = False)
    js_file.close()

def fmain():
    now = str(datetime.now())
    today = now[:4] + now[5:7] + now[8:10]
    hour = int(now[11:13])
    minute = int(now[14:16])

    while (9 <= hour <= 15):
        now = str(datetime.now())
        hour = int(now[11:13])
        minute = int(now[14:16])
        print(hour, minute)
        if hour == 15 and minute == 30:
            break
        get_ohlcv(today)
fmain()
