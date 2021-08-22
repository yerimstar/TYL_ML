import requests
import json
import time

while(1):
  url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"

  payload = "bld=dbms/MDC/STAT/standard/MDCSTAT01501&mktId=STK&trdDd=20210820&share=1&money=1&csvxls_isNo=false"
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'JSESSIONID=uuPaVBQw0sOwNTVjuSrnxaKTuXPgwSXHVCAegNdzZcbzjnNWpzTqnctlfmZQCPxS.bWRjX2RvbWFpbi9tZGNvd2FwMi1tZGNhcHAwMQ==; __smVisitorID=-vh_S9B-rJJ'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  results = json.loads(response.text)['OutBlock_1']
  print(results)
  time.sleep(72000)
