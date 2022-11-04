import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

train_data = train # train 불러오기

## 수익여부 칼럼 추가
train_수익 = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/데이콘_NH/data/train+hist+수익.csv")

train_수익 = train_수익.dropna(axis=0) # '총넣은돈-총판매된돈'컬럼에만 NaN값 존재함
train_수익_select = train_수익[["계좌ID", "종목한글명", '매수일자', 'hold_d', '총넣은돈-총판매된돈']]
len(train_data) - len(train_수익_select) # train에서 수익여부를 알 수 없는 열도 있음. (아마 종가 데이터 불러올 때 값이 없었던 듯)
train_수익추가 = pd.merge(train_data, train_수익_select, how = "left",
                      on = ["계좌ID", "종목한글명", '매수일자','hold_d']) # train데이터 원래 컬럼이 이거 4개

train_수익추가['수익여부'] = train_수익추가['총넣은돈-총판매된돈'].apply(lambda x: 1 if x < 0 else 0) # 수익 1 손해 0

train_수익추가['장투 or 단투'] = train_수익추가['hold_d'].apply(lambda x : 1 if x > 22 else 0)
계좌ID_투자평균 = train_수익추가.groupby(['계좌ID'])[['장투 or 단투']].mean().reset_index()
계좌ID_투자평균['장투 or 단투(mean)'] = 계좌ID_투자평균['장투 or 단투'].apply(lambda x : 1 if x > 0.5 else 0) # 0단투 1장투
계좌ID_투자평균.drop(columns='장투 or 단투', inplace=True)
train = pd.merge(train_수익추가, 계좌ID_투자평균, how='left', on='계좌ID')
train[:2]

# 막대 그래프로 확인
x = np.arange(2)
names = ['단기투자자', '장기투자자']
values = [139.9995178153031, 196.61087453986033]

plt.bar(x, values)
plt.xticks(x, names)
plt.title('개당? 평균 수익 비교')

plt.show()

## 아이디어
train_data[train_data['bs_number'] != 0]['총투자기간'].value_counts()
a = train_data[train_data['총투자기간']=='1년 ~ 3년 미만']

#a = pd.DataFrame({'총투자기간':['6개월미만','6개월~1년 미만','1년~3년','3년~5년','5년~10년','10년 이상'], 'bs_number!=0 비율':[0.01297,0.00491,0.05532,0.08063,0.05815,0.0531]})
a = pd.DataFrame({'bs_number!=0 비율':[0.24617,0.34053,0.37438,0.40204,0.42358,0.471392]}, index=['6개월미만','6개월~1년 미만','1년~3년','3년~5년','5년~10년','10년 이상'])
a.plot.bar()
