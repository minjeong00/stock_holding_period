import pandas as pd
import datetime
import requests
from bs4 import BeautifulSoup

# 코랩ver (데이터 폐기)
train = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/데이콘_NH/stk_hld_train.csv")
test = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/데이콘_NH/stk_hld_test.csv")

## 주식장이 열리는 날 구하기
# 토요일, 일요일
sat = pd.date_range(start='2016-01-01', end='2020-12-31', freq='W-SAT')
sun = pd.date_range(start='2016-01-01', end='2020-12-31', freq='W-SUN')
# 데이터 모양 변경
def make_list(day):
  day_list = []
  for i in range(len(day)):
    day_list.extend([str(day[i])[:4] + str(day[i])[5:7] + str(day[i])[8:10]])
  return day_list

saturday = make_list(sat)
sunday = make_list(sun)

def get_request_query(url, operation, params, serviceKey):
    import urllib.parse as urlparse
    params = urlparse.urlencode(params)
    request_query = url + '/' + operation + '?' + params + '&' + 'serviceKey' + '=' + serviceKey
    return request_query


# 공휴일 데이터 받아오기
holiday = []
# 요청 URL과 오퍼레이션
url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService'
operation = 'getHoliDeInfo'  # 국경일 + 공휴일 정보 조회 오퍼레이션

# 파라미터
servicekey = 'NbhsvEY2W5YDFECTk8ljQiUzw9vFM0TRPr2%2F6ujy7X0fff94I1GKbE%2FWKFTHbqjBFFqgw7kCE4k4POgt9K4iGA%3D%3D'
solYear = ['2016', '2017', '2018', '2019', '2020']
solMonth = ['01', '02', '03', '04', '05', '06', '08', '09', '10', '11', '12']  # 월

for year in solYear:
    for month in solMonth:
        request_query = url + '/' + operation + '?' + 'solYear' + '=' + year + '&' + 'solMonth' + '=' + month + '&' + 'serviceKey' + '=' + servicekey
        res = requests.get(url=request_query)

        soup = BeautifulSoup(res.content, 'html.parser')
        if soup.find('locdate') == None:
            continue
        else:
            mydate = soup.find_all("locdate")
            for date in mydate:
                holiday.extend([date.string])

# 주식 장이 열리지 않는 날
close_day = []
for hol in set(holiday + saturday + sunday): # 중복제거
  close_day.append(hol)

all = pd.date_range(start='2016-01-01', end='2020-12-31')
all_day = make_list(all)

# 주식 장이 열리는 날
open_day = list(set(all_day) - set(close_day))

## 매도일 구하기
open_day.sort()
open_day = list(map(int, open_day))
매도일 = []
for i in range(len(train)):
  a = open_day.index(train['byn_dt'][i])
  매도일.append(open_day[a+train['hold_d'][i]])

train['매도일'] = 매도일

## hist_d 구하기
hist_d = []

for i in range(len(train)):
  if str(매도일[i])[:4] == '2016':
    올해보유일 = open_day.index(train['매도일'][i]) - open_day.index(int(str(매도일[i])[:4] + '0104'))
    if 올해보유일 < train['hold_d'][i]: # 전연도부터보유
      hist_d.append(train['hold_d'][i] - 올해보유일)
    else:
      hist_d.append(0)

  else:
    올해보유일 = open_day.index(train['매도일'][i]) - open_day.index(int(str(매도일[i])[:4] + '0102'))
    if 올해보유일 < train['hold_d'][i]: # 전연도부터보유
      hist_d.append(train['hold_d'][i] - 올해보유일)
    else:
      hist_d.append(0)

train['hist_d'] = hist_d
