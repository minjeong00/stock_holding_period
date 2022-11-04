import numpy as np


def sex(x):
    if x == 1:
        return '남자'
    elif x == 2:
        return '여자'
    else:
        return np.nan


def age_to_obj(x):
    if x == 1:
        return '20~ 25세'
    elif x == 2:
        return '25~30세'
    elif x == 3:
        return '30~35세'
    elif x == 4:
        return '35~40세'
    elif x == 5:
        return '40~45세'
    elif x == 6:
        return '45~50세'
    elif x == 7:
        return '50~55세'
    elif x == 8:
        return '55~60세'
    elif x == 9:
        return '60~65세'
    else:
        return np.nan


def invest_pre(x):
    if x == 1:
        return "안정형"
    elif x == 2:
        return "안정추구형"
    elif x == 3:
        return "위험중립형"
    elif x == 4:
        return "적극투자형"
    elif x == 5:
        return "공격투자형"
    elif x == 9:
        return "전문투자가형"
    elif x == 0:
        return "정보제공비동의"
    elif x == 99:
        return "미정의"
    else:
        return np.nan


def asset_amount_obj(x):
    if x == 1:
        return '0원이상 1천만원미만'
    elif x == 2:
        return '1천만원이상 3천만원미만'
    elif x == 3:
        return '3천만원이상 5천만원미만'
    elif x == 4:
        return '5천만원이상 1억원미만'
    elif x == 5:
        return '1억원이상 3억원미만'
    elif x == 6:
        return '3억원이상'
    else:
        return np.nan


def main_target_obj(x):
    if x == 1:
        return 'only_CMA'
    elif x == 2:
        return '국내주식'
    elif x == 3:
        return '해외주식'
    elif x == 4:
        return '선물옵션'
    elif x == 5:
        return '금속'
    elif x == 6:
        return '국내채권'
    elif x == 7:
        return '해외채권'
    elif x == 8:
        return '펀드'
    elif x == 9:
        return 'ELS/DLS'
    elif x == 10:
        return '신탁_퇴직연금'
    elif x == 11:
        return 'RP'
    elif x == 12:
        return '발행어음'
    elif x == 14:
        return 'WRAP'
    elif x == 15:
        return '신용대출'
    elif x == 99:
        return '미정의'
    else:
        return np.nan


def LIFE_obj(x):
    if x == 2:
        return '사회초년생'
    elif x == 3:
        return '가족형성기_남자'
    elif x == 4:
        return '가족형성기_여자'
    elif x == 5:
        return '가족성숙기_직장인_남자'
    elif x == 6:
        return '가족성숙기_주부_여자'
    elif x == 7:
        return '가족성숙기_기타_남자'
    elif x == 8:
        return '가족성숙기_기타_여자'
    elif x == 9:
        return '은퇴기'
    else:
        return np.nan


def client_obj(x):
    if x == 1:
        return '탑클래스(10억이상 or 수익기여도 5백만원 이상)'
    elif x == 2:
        return '골드(3억이상 or 수익기여도 3백만원 이상)'
    elif x == 3:
        return '로얄(자산1억이상 or 수익기여도 1백만원 이상)'
    elif x == 4:
        return '그린(자산3천이상 or 수익기여도 5십만원 이상)'
    elif x == 5:
        return '블루(자산1천이상 or 수익기여도 1십만원 이상)'
    elif x == 9:
        return '등급 미정의'
    elif x == 99:
        return '미정의(결측치)'
    else:
        return np.nan


def invest_total_obj(x):
    if x == 1:
        return '6개월미만'
    elif x == 2:
        return '6개월 미만 ~ 1년 미만'
    elif x == 3:
        return '1년 ~ 3년 미만'
    elif x == 4:
        return '3년 ~ 5년 미만'
    elif x == 5:
        return '5년 ~ 10년 미만'
    elif x == 6:
        return '10년 이상'
    else:
        return np.nan


def main_target_obj(x):
    if x == 1:
        return "건설업"
    elif x == 2:
        return "금융업"
    elif x == 3:
        return "기계"
    elif x == 4:
        return "방송/통신"
    elif x == 5:
        return "서비스/오락/문화"
    elif x == 6:
        return "운송/운수"
    elif x == 7:
        return "유통"
    elif x == 8:
        return "의료/의약"
    elif x == 9:
        return "전기/전자"
    elif x == 10:
        return "제조"
    elif x == 11:
        return "철강"
    elif x == 12:
        return "화학"
    elif x == 13:
        return "IT"
    elif x == 14:
        return "기타"
    elif x == 15:
        return "혼합"
    elif x == 16:
        return "비매매"
    else:
        return np.nan


def iem_subject(x):
    if x == 1:
        return "건설"
    elif x == 2:
        return "금융"
    elif x == 3:
        return "기계"
    elif x == 4:
        return "통신"
    elif x == 5:
        return "서비스"
    elif x == 6:
        return "운송"
    elif x == 7:
        return "유통"
    elif x == 8:
        return "의료"
    elif x == 9:
        return "전기"
    elif x == 10:
        return "제조"
    elif x == 11:
        return "철강"
    elif x == 12:
        return "화학"
    elif x == 13:
        return "IT"
    elif x == 14:
        return "기타"
    else:
        return np.nan


def iem_all_money(x):
    if x == 1:
        return "대형주"
    elif x == 2:
        return "중형주"
    elif x == 3:
        return "소형주"
    elif x == 99:
        return "기타"
    else:
        return np.nan


def iem_market(x):
    if x == 1:
        return "대기업"
    elif x == 2:
        return "중견기업or밴처기업"
    elif x == 99:
        return "기타"
    else:
        return np.nan