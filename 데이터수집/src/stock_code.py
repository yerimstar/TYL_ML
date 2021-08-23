import requests
import json
import csv
f = open('../data/stock_code.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd?bld=dbms/MDC/STAT/standard/MDCSTAT01901&mktId=ALL&share=1&csvxls_isNo=false"
response = requests.post(url)
results = json.loads(response.text)['OutBlock_1']
wr.writerow(['code','name','market'])
for result in results:
    code = result['ISU_SRT_CD']
    name = result['ISU_ABBRV']
    type = result['MKT_TP_NM']
    wr.writerow([code,name,type])
f.close()