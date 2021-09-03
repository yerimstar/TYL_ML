# -*- coding : utf-8 -*-
import FinanceDataReader as fdr
import xgboost
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from joblib import dump
from datetime import datetime

now = datetime.now()
today = ("%s%s%s%s%s%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second))

input_file_name1 = '../../종목코드/KOSPI_Code.csv'
input_file_name2 = '../../종목코드/KOSDAQ_Code.csv'
output_file_name = "XGBoost_save_" +  str(today) + ".txt"
output_file = open('../result/' + output_file_name, "w", encoding="utf-8")
output_file.write("{}\t{}\t{}\n".format("Code","max_depth","test_score"))
output_file.close()

error_file_name = "RF_ValueError_" +  str(today) + ".txt"
error_file = open('../result/' + error_file_name, "w", encoding="utf-8")
error_file.write("{}\n".format("Code"))
error_file.close()

def fget_code(input_file_name):
    input_file = open(input_file_name,"r",encoding='utf-8')
    input_text = input_file.read()
    lines = input_text.splitlines()
    code_list = []
    for line in lines[1:]:
        code = line.split(',')[0]
        code_list.append(code)
    return code_list

def fget_model(code):
    print("code = ",code)
    stock_data = fdr.DataReader(code, '2018-07-31', '2021-07-31')
    stock_data['Predict'] = stock_data['Close'].shift(-1)  # 예측값(y값) 채워넣기
    stock_data.dropna(inplace=True)  # null 값 제거
    feature_names = ['Open', 'High', 'Low', 'Close', 'Volume', 'Change']  # X값이 될 수 있는 항목들
    x = stock_data[feature_names]
    y = stock_data['Predict']
    mae_list = []
    mae2_list = []
    for i in range(1, 20):
        model = xgboost.XGBRegressor(max_depth = i,learning_rate = 0.2)
        try:
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=21)
        except ValueError:
            error_file = open('../result/' + error_file_name, "a", encoding="utf-8")
            error_file.write("{}\n".format(code))
            error_file.close()
            return
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        y_train_pred = model.predict(x_train)
        mae = mean_absolute_error(y_test, y_pred)
        mae2 = mean_absolute_error(y_train, y_train_pred)
        mae_list.append(mae)
        mae2_list.append(mae2)
    mdepth = mae_list.index(min(mae_list)) + 1
    print("mdepth = ", mdepth)
    model = xgboost.XGBRegressor(max_depth = mdepth,learning_rate = 0.2)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=21)
    model.fit(x_train, y_train)
    score = model.score(x_test, y_test)
    print("score =",score)

    output_file = open('../result/' + output_file_name, "a", encoding="utf-8")
    output_file.write("{}\t{}\t{}\n".format(code,mdepth,score))
    output_file.close()

    save_model_name = code + '.joblib'
    dump(model, '../save_model/' + save_model_name)

code_list = []
code_list += fget_code(input_file_name1)
code_list += fget_code(input_file_name2)

for i in range(295,len(code_list)):
    print("num = ",i)
    fget_model(code_list[i])