import pandas as pd
import streamlit as st
import FinanceDataReader as fdr
import matplotlib.pyplot as plt

from datetime import datetime
from dateutil.relativedelta import *
# import mplfinance as mpf
from mpl_finance import candlestick2_ohlc
# import matplotlib.ticker as ticker
import plotly.graph_objects as go

import plotly.express as px

st.title('국내 주식 현황입니다.')
Stockcode = pd.read_csv('data/Stockcode.csv')
Stockcode.set_index('Name', inplace=True)
Name = st.text_input('Code Name')
Code_name_list = Stockcode.index.tolist()

if Name in Code_name_list:
    code_num = Stockcode.at[Name, 'Symbol']
    end = datetime.now().date()
    start = end+relativedelta(years=-1)
    df = fdr.DataReader(code_num, start, end)
    col1, col2, col3 = st.columns(3)
    col1.metric("현재 주식가격",format(df['Close'].tail(1)[0], ',')+'원', "%d원" %(df['Close'].diff().tail(1)[0]),delta_color="inverse")
    col2.metric("전일 대비 가격", "%d원" %(df['Close'].diff().tail(1)[0]), "%.2f%%" %(df['Change'].tail(1)[0] * 100),delta_color="inverse")
    col3.metric("현재 거래량", format(df['Volume'].tail(1)[0], ','),"%.2f%%" %(df['Volume'].pct_change().tail(1)[0] * 100),delta_color="inverse")

    fig = go.Figure(data=[go.Candlestick(
    x=df.index,
    open=df['Open'], high=df['High'],
    low=df['Low'], close=df['Close'],
    increasing_line_color= 'red', decreasing_line_color= 'blue',
    showlegend = False
    )])

    fig.update_layout(title='{} 주가 chart'.format(Name))
    st.plotly_chart(fig, use_container_width=False)

elif Name not in Code_name_list:
    st.text('검색하신 주식 종목이 없습니다. 정확하게 입력해주세요.')
