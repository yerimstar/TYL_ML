import FinanceDataReader as fdr
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

code = '005930'

today = datetime.date.today()
month_before = datetime.datetime.now()-relativedelta(months=1)
month_before = month_before.date()

data = fdr.DataReader(code,month_before,today) # 종목코드 입력
data.to_csv('../data/data_month_' + code + '.csv')
csv_data = pd.read_csv('../data/data_month_' + code + '.csv')
json_data = csv_data.to_json('../data/data_month_' + code + '.json',orient='records')
