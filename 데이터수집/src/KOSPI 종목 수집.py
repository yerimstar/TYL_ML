import requests
import json
import csv
f = open('KOSPI_Code.csv','w',encoding='utf-8',newline='')
wr = csv.writer(f)
url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd?bld=dbms/MDC/STAT/standard/MDCSTAT01901&mktId=STK&share=1&csvxls_isNo=false"
response = requests.post(url)
results = json.loads(response.text)['OutBlock_1']
wr.writerow(['단축코드','한글종목약명','시장구분'])
for result in results:
    code = result['ISU_SRT_CD']
    name = result['ISU_ABBRV']
    type = result['MKT_TP_NM']
    wr.writerow([code,name,type])
f.close()
