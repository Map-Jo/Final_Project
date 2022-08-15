# 코사인 유사도 코드출처 : https://teddylee777.github.io/pandas/cos-sim-stock

import FinanceDataReader as fdr
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import datetime

st.set_page_config(
    page_title="반포자이까지 한걸음",
    page_icon= "chart_with_upwards_trend",
    layout="wide",
)

st.sidebar.markdown("# Predict Local Stockcode 📊")

st.title('국내주식 종목의 주가를 예측해 보세요 📈')


Stockcode = pd.read_csv('data/Stockcode.csv')
Stockcode.set_index('Name', inplace=True)
Name = st.text_input('Code Name').upper()

Code_name_list = Stockcode.index.tolist()


if Name in Code_name_list:
    code_num = Stockcode.at[Name, 'Symbol']
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
        target = data['Close'].iloc[i:i+window_size]
        target = (target - target.min()) / (target.max() - target.min())
        cos_similarity = cosine_similarity(base, target)
        sim_list.append(cos_similarity)

    top = pd.Series(sim_list).sort_values(ascending=False).head(1).index[0]

    idx=top
    target = data['Close'].iloc[idx:idx+window_size+5]
    target = (target - target.min()) / (target.max() - target.min())

    fig = plt.figure(figsize=(20,10))
    plt.plot(base.values, label='base', color='grey')
    plt.plot(target.values, label='target', color='orangered')
    plt.xticks(np.arange(len(target)), list(target.index.strftime('%Y-%m-%d')), rotation=45)
    plt.axvline(x=len(base)-1, c='grey', linestyle='--')
    plt.axvspan(len(base.values)-1, len(target.values)-1, facecolor='ivory', alpha=0.7)
    plt.legend()
    st.pyplot(fig)

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

    if pred > 0:
        plus_money = yesterday_close + predict
        plus_money = format(int(plus_money), ',')
        st.markdown(f'예상 주가는 **{plus_money}원** 입니다.')
    elif pred < 0:
        minus_money = yesterday_close - predict
        minus_money = format(int(minus_money), ',')
        st.markdown(f'예상 주가는 **{minus_money}원** 입니다.')
    else:
        st.markdown(yesterday_close)

elif Name not in Code_name_list:
    st.text('검색하신 주식 종목이 없습니다. 정확하게 입력해주세요.')