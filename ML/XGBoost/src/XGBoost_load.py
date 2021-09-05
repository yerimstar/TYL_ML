import FinanceDataReader as fdr
import json
from sklearn.metrics import mean_absolute_error
from joblib import load
from datetime import datetime

data = {}
now = datetime.now()
today = ("%s%s%s%s%s%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second))

input_file_name = '../../종목코드/test_stock_code.csv'
output_file_name = "XGBoost_load_" +  str(today) + ".txt"
output_file = open('../result/' + output_file_name, "w", encoding="utf-8")
output_file.write("{}\t{}\t{}\t{}\n".format("Code","predict_data","percentage","mae"))
output_file.close()

def fget_code(input_file_name):
    input_file = open(input_file_name,"r",encoding='utf-8')
    input_text = input_file.read()
    lines = input_text.splitlines()
    code_list = []
    for line in lines[1:]:
        code = line.split(',')[0]
        code_list.append(code)
    return code_list

def fget_predict_value(code):
    print("code =",code)
    date = str(now.year) + '-' + str(now.month) + '-' + str(now.day-2) # 장이 닫힌 시점에 내일 주가 예측 데이터 수집
    stock_data = fdr.DataReader(code,date)
    load_file_name = code +'.joblib'
    try:
        model = load('../save_model_test/'+load_file_name)
    except:
        return
    try:
        predict_data = model.predict(stock_data)
    except ValueError:
        return
    try:
        mae = mean_absolute_error(stock_data['Close'],predict_data)
    except ValueError:
        return
    print("Close data = ",stock_data['Close'][0])
    print("predict_data = ",predict_data[0])
    print("mae = ",mae)
    gap = predict_data[0] - stock_data['Close'][0]
    percentage = round((gap/stock_data['Close'][0])*100,1)
    print("percentage = ",percentage)
    output_file = open('../result/' + output_file_name, "a", encoding="utf-8")
    output_file.write("{}\t{}\t{}\t{}\n".format(code, predict_data[0],percentage, mae))
    output_file.close()
    data[code] = percentage

code_list = fget_code(input_file_name)

for code in code_list:
    fget_predict_value(code)

with open("../result/XGBoost_data.json", "w") as f:
    json.dump(data, f)



