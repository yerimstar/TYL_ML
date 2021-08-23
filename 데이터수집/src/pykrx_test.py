from pykrx import stock
from datetime import datetime

while(1):
    df_stock = stock.get_market_ohlcv_by_ticker(date="20210823",market="ALL")
    df_stock = df_stock.reset_index()
    print(df_stock)
    print(datetime.now())
    js_stock = df_stock.to_json(orient='records',force_ascii=False)
    print(js_stock)
