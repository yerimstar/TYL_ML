import FinanceDataReader as fdr
import json
from sklearn.metrics import mean_absolute_error
from joblib import load
from datetime import datetime

data = {}
now = datetime.now()
today = ("%s%s%s%s%s%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second))

input_file_name1 = '../../종목코드/KOSPI_Code.csv'
input_file_name2 = '../../종목코드/KOSDAQ_Code.csv'
output_file_name = "RF_load_" +  str(today) + ".txt"
output_file = open('../result/' + output_file_name, "w", encoding="utf-8")
output_file.write("{}\t{}\t{}\n".format("Code","predict_data","mae"))
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
    date = str(now.year) + '-' + str(now.month) + '-' + str(now.day) # 장이 닫힌 시점에 내일 주가 예측 데이터 수집
    stock_data = fdr.DataReader(code,date)
    load_file_name = code +'.joblib'
    model = load('../save_model/'+load_file_name)
    predict_data = model.predict(stock_data)
    mae = mean_absolute_error(stock_data['Close'],predict_data)
    print("predict_data = ",predict_data)
    print("mae = ",mae)
    output_file = open('../result/' + output_file_name, "a", encoding="utf-8")
    output_file.write("{}\t{}\t{}\n".format(code, predict_data, mae))
    output_file.close()

    data[code]= predict_data[0]

code_list = []
code_list += fget_code(input_file_name1)
code_list += fget_code(input_file_name2)

for code in code_list:
    fget_predict_value(code)

with open("RF_data.json", "w") as f:
    json.dump(data, f)

