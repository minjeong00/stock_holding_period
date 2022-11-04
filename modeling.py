# pip install pandas
# pip install numpy
# pip install datetime
# pip install requests
# pip install beautifulsoup4
# pip install catboost

from labeling import *
import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
import warnings
# warnings.filterwarnings('ignore')


pd.set_option("display.max_row", 300)
pd.set_option("display.max_column", 300)
pd.set_option('max_colwidth', 1000)

# colab ver
train = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/데이콘_NH/data/stk_hld_train.csv', encoding = "UTF-8")
test = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/데이콘_NH/data/stk_hld_test.csv', encoding = "UTF-8")
iem = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/데이콘_NH/data/iem_info_20210902.csv", encoding = "UTF-8")
cus = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/데이콘_NH/data/cus_info.csv", encoding = "UTF-8")
hist = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/데이콘_NH/data/stk_bnc_hist.csv", encoding = "UTF-8")
submission = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/데이콘_NH/data/sample_submission.csv', encoding = "UTF-8")

## target 설정
# target을 hold_d - hist_d 로 설정
train['hold_d-hist_d'] = train['hold_d'] - train['hist_d']

# test 데이터 컬럼명 변경
test = test.rename(columns = {'act_id' : '계좌ID', 'iem_cd' : '종목코드', 'byn_dt': '매수일자'})

# 편의를 위해 train, test 합치기 나중에 submit_id 있나 없나로 test, train 구분 하기
df = pd.concat([train,test])

# 종목정보 데이터 컬럼명 변경
iem = iem.rename(columns = {'iem_cd':'종목코드','iem_krl_nm':'종목한글명','btp_cfc_cd':'종목업종','mkt_pr_tal_scl_tp_cd':'시가총액규모유형', 'stk_dit_cd': '시장구분'})
df = pd.merge(df, iem, how = "left", on = ["종목코드"])

# cus_info데이터 컬럼명 변경
cus= cus.rename(columns = {'act_id' : '계좌ID','sex_dit_cd':'성별','cus_age_stn_cd':'연령구간',\
                                   'ivs_icn_cd' : '투자성향', 'cus_aet_stn_cd':'고객자산구간','mrz_pdt_tp_sgm_cd': '주거래상품군',\
                                   'lsg_sgm_cd' : 'LifeStage','tco_cus_grd_cd' : '고객등급', 'tot_ivs_te_sgm_cd' : '총투자기간',\
                                   'mrz_btp_dit_cd' : '주거래업종구분'})

df=pd.merge(df, cus, on = ["계좌ID"], how='left')

## 수치화 데이터 한글로 전황
df['성별'] = df['성별'].apply(sex)
df['연령구간'] = df['연령구간'].apply(age_to_obj)
df['고객자산구간'] = df['고객자산구간'].apply(asset_amount_obj)
df['주거래상품군'] = df['주거래상품군'].apply(main_target_obj)
df['투자성향'] = df['투자성향'].apply(invest_pre)
df['LifeStage'] = df['LifeStage'].apply(LIFE_obj)
df['고객등급'] = df['고객등급'].apply(client_obj)
df['총투자기간'] = df['총투자기간'].apply(invest_total_obj)
df['주거래업종구분'] = df['주거래업종구분'].apply(main_target_obj)
df['종목업종'] = df['종목업종'].apply(iem_subject)
df['시가총액규모유형'] = df['시가총액규모유형'].apply(iem_all_money)
df['시장구분'] = df['시장구분'].apply(iem_market)

# 국내주식 잔고이력 데이터 컬럼명 변경
hist= hist.rename(columns = {'act_id': '계좌ID', 'bse_dt' : '기준일자', 'iem_cd' : '종목코드',\
                                    'bnc_qty' : '잔고수량', 'tot_aet_amt':'잔고금액', 'stk_par_pr' : '액면가'})

hist['현재개당주가'] = hist["잔고금액"] / hist["잔고수량"]


# #다시 test, train 구분 해주기
train = df[df['submit_id'].isna()]
test = df[df['submit_id'].notna()]

train_after = pd.merge(train, hist, how = "left", on = ["계좌ID", "종목코드"])
test_after = pd.merge(test, hist, how = "left", on = ["계좌ID", "종목코드"])

# 눈에 들어오기 쉽게 컬럼들의 순서를 임시로 변경
train_after=train_after[['계좌ID','성별','연령구간','투자성향','고객자산구간','주거래상품군','LifeStage',
                         '고객등급','총투자기간','주거래업종구분','종목코드','종목한글명','종목업종','시가총액규모유형',
                         '시장구분','매수일자','기준일자','잔고수량','잔고금액','액면가','현재개당주가','hist_d',
                         'hold_d','submit_id']]
test_after=test_after[['계좌ID','성별','연령구간','투자성향','고객자산구간','주거래상품군','LifeStage',
                       '고객등급','총투자기간','주거래업종구분','종목코드','종목한글명','종목업종','시가총액규모유형',
                       '시장구분','매수일자','기준일자','잔고수량','잔고금액','액면가','현재개당주가','hist_d',
                       'hold_d','submit_id']]

## bs_number 구하기
# train에 hist.csv 병합 후 파일에 filter 적용하여 알맞는 데이터만 추출
train_after['매수일자_count'] = train_after['매수일자'].apply(lambda x : open_day.index(x))
train_after['기준일자_count'] = train_after['기준일자'].apply(lambda x : open_day.index(x))
train_after['filter'] = train_after['기준일자_count'] - train_after['매수일자_count']
train_after = train_after[train_after['filter'] <= train_after['hold_d']]
train_after = train_after[train_after['filter'] >= 0]
train_after.drop(columns=['매수일자_count', '기준일자_count', 'filter'], inplace=True)
train_after.reset_index(drop=True, inplace=True)
print(train_after.shape)
train_after.head()

train_after['매수일자_index'] = train_after['매수일자'].apply(lambda x : open_day.index(x))
train_after['매수일자_index_+hold_d'] = train_after['hold_d'] + train_after['매수일자_index']
train_after['매도일'] = train_after['매수일자_index_+hold_d'].apply(lambda x : open_day[x])
train_after.drop(columns=['매수일자_index','매수일자_index_+hold_d' ], inplace=True)
train_after['매수한년도'] = train_after['매수일자'].apply(lambda x : int(str(x)[:4]))
train_after['매도한년도'] = train_after['매도일'].apply(lambda x : int(str(x)[:4]))
train_after['매도한전년도'] = train_after['매도한년도'].apply(lambda x : x-1)
train_after = train_after[train_after['매수한년도'] < train_after['매도한년도']]
train_after['매도한전년도주식마지막날'] = train_after['매도한전년도'].apply(lambda x : int(each_year_lastday(x)))
train_after_filter = train_after[train_after['매도한전년도주식마지막날'] >= train_after['기준일자']]

# bs_number 컬럼 추가
train_after_filter = train_after_filter.groupby(['계좌ID','종목코드','매수일자']).count()
train_after_filter = train_after_filter.reset_index(drop=False)
train_after_filter['bs_number'] = train_after_filter['성별']

train_after_filter = train_after_filter[['계좌ID','종목코드','매수일자','bs_number']]

train = pd.merge(train, train_after_filter, how='left', on=['계좌ID','종목코드','매수일자'])
train['bs_number'].fillna(0, inplace=True)

## test 동일하게 적용
# hist.csv병합 후 알맞는 hist만 필터링
test_after['매수일자_count'] = test_after['매수일자'].apply(lambda x : open_day.index(x))
test_after['기준일자_count'] = test_after['기준일자'].apply(lambda x : open_day.index(x))
test_after['filter'] = test_after['기준일자_count'] - test_after['매수일자_count']
test_after = test_after[test_after['filter'] >= 0 ]
test_after.drop(columns=['매수일자_count', '기준일자_count', 'filter'], inplace=True)
test_after.reset_index(drop=True, inplace=True)

# test데이터의 매도하기 전년도 까지 주식을 손댄횟수(bs_number) 추가
test_sold_day = test_after.groupby(['계좌ID','종목코드','매수일자']).count()
test_sold_day = test_sold_day.reset_index(drop=False)
test_sold_day['bs_number'] = test_sold_day['성별']
test_sold_day = test_sold_day[['계좌ID','종목코드','매수일자','bs_number']]
test = pd.merge(test, test_sold_day, how='left', on=['계좌ID','종목코드','매수일자'])

## 거래량 구하기
id_거래량_value = hist['계좌ID'].value_counts().values
id_거래량_index = hist['계좌ID'].value_counts().index
id_거래량 = pd.DataFrame({'계좌ID' : id_거래량_index, '거래량' : id_거래량_value})
# train에 추가
train = pd.merge(train, id_거래량, how = "left", on = ["계좌ID"])
# test에 추가
test = pd.merge(test, id_거래량, how = "left", on = ["계좌ID"])

## model 돌리기 전 데이터 최종 병합
test_data = test
train_data = train

# train_data에서 Y값을 추출한 후 hold_d, hold_d-hist_d column 삭제

train_label = train_data["hold_d-hist_d"]
train_data.drop(["hold_d", "hold_d-hist_d"], axis = 1, inplace = True)

hist = hist.fillna(0)

# train + 고객정보 + 주식정보 + 국내 주식 잔고 이력
train_data = pd.merge(train_data, hist, how = "left", on = ["계좌ID", "종목코드"])
train_data = train_data[(train_data["매수일자"] == train_data["기준일자"])] # byn_dt 매수일자 == 기준일자(국내 주식잔고이력)
train_data.reset_index(drop = True, inplace = True)

test_data = pd.merge(test_data, hist, how = "left", on = ["계좌ID", "종목코드"])
test_data = test_data[(test_data["매수일자"] == test_data["기준일자"])]
test_data.reset_index(drop = True, inplace = True)

# 최종 적으로 학습 시킬 columns 만 남기겠습니다.
train_data = train_data.drop(["계좌ID","주거래상품군", "종목코드", "매수일자", "기준일자",
                              "submit_id",'액면가'], axis = 1)
test_data = test_data.drop(["계좌ID","주거래상품군", "종목코드", "매수일자", "submit_id",
                            "hold_d", "기준일자","hold_d-hist_d",'액면가'], axis = 1)

# index초기화
train_data.reset_index(drop = True, inplace=True)
train_label.reset_index(drop = True, inplace=True)

## model 학습
# 모델 학습
cat = CatBoostRegressor(verbose=100,
                        eval_metric = 'RMSE',
                        iterations = 1000,
                        learning_rate = 0.005)
cat.fit(train_data, train_label,
        early_stopping_rounds=300,
        cat_features = [1,2,3,4,5,6,7,8,9,10,11,12]) # 카테고리컬 변수의 컬럼 지정

# 이상치 구하기
preds = cat.predict(test_data)

preds = list(np.round(preds))
preds_df = pd.DataFrame({'hold_d-hist_d':preds})
preds_df['hold_d-hist_d'] = preds_df['hold_d-hist_d'].apply( lambda x : 146 if x > 146 else x )

## hold_d 구하기
# test에 예측되어진 hold_d 컬럼 추가 및 submission에 값 넣기
test_data['hold_d'] = preds_df['hold_d-hist_d'] + test_data['hist_d']
submission['hold_d'] = test_data['hold_d']
