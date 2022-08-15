from sklearn.svm import SVR
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import seaborn as sns
import koreanize_matplotlib
from sklearn.preprocessing import MinMaxScaler
import datetime
import streamlit as st


Stockcode = pd.read_csv('data/stockcode_pdr.csv')
sub_df = Stockcode.copy()
sub_df.set_index('name', inplace=True)
name = st.text_input('Code Name')
Code_name_list = sub_df.index.tolist()

if name in Code_name_list:
    code_num = sub_df.at[name, 'code']

    start = datetime.datetime.now()-datetime.timedelta(days=94)
    start = start.strftime('%Y-%m-%d')

    stock_data = pdr.get_data_yahoo(code_num, start)
    st.text(stock_data.shape)

    if stock_data.shape[0] == 64:

        mms = MinMaxScaler()
        stock_data[['Adj Close_mm']] = mms.fit_transform(stock_data[['Adj Close']])

        stock_data_adj_close = stock_data['Adj Close_mm']
        stock_data_adj_close = stock_data_adj_close.values

        days = []
        j=1
        for j in range(len(stock_data)):
            days.append([int(j+1)])
            j=j+1

        rbf_svr = SVR(kernel='rbf', C=1000, gamma=0.05)
        rbf_svr.fit(days,stock_data_adj_close)

        SVR(C=1000, cache_size=200,coef0=0.0, degree=3,epsilon=0.1, gamma=0.05,
        kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

        day = [[len(days) + 1]]

        predict = mms.inverse_transform(rbf_svr.predict(day).reshape(-1,1))
        predict = format(int(predict), ',')
        preidct = str(predict)

        stock_data['rbf'] = rbf_svr.predict(days)
        
        fig = plt.figure(figsize=(15,8))
        sns.scatterplot(x=stock_data.index, y=stock_data['Adj Close_mm'], data=stock_data,label='Adj Close',color='k')
        sns.lineplot(x=stock_data.index, y=stock_data['rbf'], data=stock_data,label='rbf')
        plt.title(f'{name} 주가 예측 그래프')

        st.pyplot(fig)
        st.text(f'{name}의 내일 예상 주가는 {predict}원 입니다.')

    elif stock_data.shape[0] < 65:
        st.write(f'{name}은 최근에 상장한 주식으로 예상됩니다.')
        st.write('예측하기에는 데이터가 부족하네요...')
        st.write('충분한 데이터가 모일 때까지 조금만 기다려 주세요~')


elif name not in Code_name_list:
    st.text('검색하신 주식 종목이 없습니다. 정확하게 입력해주세요.')

# st.button("button 1")
# st.text("")
# st.button("button 2")