import json
from pykrx import stock
from datetime import datetime

while(1):
    df_stock = stock.get_market_ohlcv_by_ticker(date="20210823",market="ALL")
    df_stock = df_stock.reset_index()
    print(datetime.now())
    df_stock.columns = ['code','open','high','low','close','volume','amount','rate']
    js_stock = df_stock.to_json(orient='records',force_ascii=False)
    with open("./stock_data.json", "w",encoding='utf-8') as json_file:
        json.dump(js_stock, json_file,ensure_ascii = False)
