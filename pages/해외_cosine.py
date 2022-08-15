# 환율 변환 코드출처: https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=nanayagoon&logNo=221246948133

import pandas as pd
import streamlit as st
import FinanceDataReader as fdr
import urllib.request
import datetime
import numpy as np
import matplotlib.pyplot as plt

page = urllib.request.urlopen("https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%ED%99%98%EC%9C%A8")
text = page.read().decode("utf8")

where = text.find('class="grp_info"> <em>')
start_of_time = where + 22
end_of_time = start_of_time + 16
prin = text[start_of_time:end_of_time]

usdwhere = text.find('<span>미국 <em>USD</em></span></a></th> <td><span>')
usdletter =  text[usdwhere+48] + text[usdwhere+50:usdwhere+56]


Stockcode = pd.read_csv('data/oversea_stockcode.csv')
Stockcode.set_index('Symbol', inplace=True)
Name = st.text_input('Code Name', 'ticker를 입력해주세요.').upper()
Code_name_list = Stockcode.index.tolist()
Stockcode['ticker'] = Stockcode.index

if Name in Code_name_list:
    code_num = Stockcode.at[Name, 'ticker']
    data = fdr.DataReader(code_num)
    startdate = (datetime.datetime.now()-datetime.timedelta(days=31)).strftime('%Y-%m-%d')
    enddate = datetime.datetime.now().strftime('%Y-%m-%d')
    data_ = data.loc[startdate:enddate]
    close = data_['Close']
    base = (close - close.min()) / (close.max() - close.min())
    window_size = len(base)
    next_date = 5
    moving_cnt = len(data) - window_size - next_date - 1
    def cosine_similarity(x, y):
        return np.dot(x, y) / (np.sqrt(np.dot(x, x)) * np.sqrt(np.dot(y, y)))

    sim_list = []

    for i in range(moving_cnt):
        # i 번째 인덱스 부터 i+window_size 만큼의 범위를 가져와 target 변수에 대입합니다
        target = data['Close'].iloc[i:i+window_size]
        
        # base와 마찬가지로 정규화를 적용하여 스케일을 맞춰 줍니다
        target = (target - target.min()) / (target.max() - target.min())
        
        # 코사인 유사도를 계산합니다
        cos_similarity = cosine_similarity(base, target)
        
        # 계산된 코사인 유사도를 추가합니다
        sim_list.append(cos_similarity)

    top = pd.Series(sim_list).sort_values(ascending=False).head(1).index[0]

    idx=top

    # target 변수에 종가 데이터의 [기준 인덱스] 부터 [기준 인덱스 + window_size + 예측(5일)] 데이터를 추출합니다
    target = data['Close'].iloc[idx:idx+window_size+5]

    # 정규화를 적용합니다
    target = (target - target.min()) / (target.max() - target.min())

    # 결과를 시각화합니다
    fig = plt.figure(figsize=(20,10))
    plt.plot(base.values, label='base', color='grey')
    plt.plot(target.values, label='target', color='orangered')
    plt.xticks(np.arange(len(target)), list(target.index.strftime('%Y-%m-%d')), rotation=45)
    plt.axvline(x=len(base)-1, c='grey', linestyle='--')
    plt.axvspan(len(base.values)-1, len(target.values)-1, facecolor='ivory', alpha=0.7)
    plt.legend()
    st.pyplot(fig)

    money = data['Close'].tail(1)
    k_money = float(money)*float(usdletter)
    k_money = round(k_money,2)


    period=5
    preds = data['Change'][idx+window_size: idx+window_size+period]
    cos = round(float(pd.Series(sim_list).sort_values(ascending=False).head(1).values), 2)
    st.markdown(f'현재 주식 상황과 **{cos} %** 유사한 시기의 주식 상황입니다.')
    future = round(preds.mean()*100, 2)
    if future > 0:
        st.markdown(f'위의 주식 상황을 바탕으로 앞으로 **{Name}** 주식은 **{future}%** 상승할 것으로 보입니다.')
    elif future < 0:
        st.markdown(f'위의 주식 상황을 바탕으로 앞으로 **{Name}** 주식은 **{future}%** 하락할 것으로 보입니다.')

    pred = preds.mean()
    predict = data['Close'].tail(1).values * preds.mean()
    yesterday_close = data['Close'].tail(1).values
    k_yesterday = k_money

    if pred > 0:
        plus_money = yesterday_close + predict
        plus_money = format(int(plus_money), ',')
        k_plus_money = k_yesterday + predict
        k_plus_money = format(int(k_plus_money), ',')
        st.markdown(f'예상 주가는 **{plus_money}$ ({k_plus_money}원)** 입니다.')

    elif pred < 0:
        minus_money = yesterday_close - predict
        minus_money = format(int(minus_money), ',')
        k_minus_money = k_yesterday - predict
        k_minus_money = format(int(k_minus_money), ',')

        st.markdown(f'예상 주가는 **{minus_money}$ ({k_minus_money}원)** 입니다.')
    else:
        st.markdown(yesterday_close)


    st.text(prin +'의 KEB하나은행 환율정보 입니다.')
    st.text('현재 1$당 '+str(usdletter)+'원 입니다.')
elif Name not in Code_name_list:
    st.text('검색하신 주식 종목이 없습니다. 정확하게 입력해주세요.')