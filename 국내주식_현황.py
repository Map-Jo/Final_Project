import pandas as pd
import streamlit as st
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
# import koreanize_matplotlib
import plotly.express as px
import time

start = time.time()
st.set_page_config(
    page_title="반포자이까지 한걸음",
    page_icon= "chart_with_upwards_trend",
    layout="wide",
)

st.sidebar.markdown("# Local Stocks 📊")

st.title('Local Stocks 📈')
Stockcode = pd.read_csv('data/Stockcode.csv')
Stockcode.set_index('Name', inplace=True)
Name = st.text_input('Code Name')
Code_name_list = Stockcode.index.tolist()

if Name in Code_name_list:
    code_num = Stockcode.at[Name, 'Symbol']
    df = fdr.DataReader(code_num)
    col1, col2, col3 = st.columns(3)
    col1.metric("현재 주식가격",format(df['Close'].tail(1)[0], ',')+'원', "%d원" %(df['Close'].diff().tail(1)[0]))
    col2.metric("현재 거래량", format(df['Volume'].tail(1)[0], ','),"%.2f%%" %(df['Volume'].pct_change().tail(1)[0] * 100))
    col3.metric("전일 대비 가격", "%d원" %(df['Close'].diff().tail(1)[0]), "%.2f%%" %(df['Change'].tail(1)[0] * 100))

elif Name not in Code_name_list:
    st.text('검색하신 주식 종목이 없습니다. 정확하게 입력해주세요.')

a = "time :", time.time() - start
st.text(a)

('time :', 0.2275242805480957)