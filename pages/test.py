import pandas as pd
import streamlit as st
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import koreanize_matplotlib
import plotly.express as px
from pandas_datareader import data as pdr


st.title('Local Stocks 📈')
Stockcode = pd.read_csv('data/stockcode_pdr.csv')
sub_df = Stockcode.copy()
sub_df.set_index('name', inplace=True)
name = st.text_input('Code Name')
Code_name_list = sub_df.index.tolist()

if name in Code_name_list:
    code_num = sub_df.at[name, 'code']
    df = pdr.get_data_yahoo(code_num)
    df
elif name not in Code_name_list:
    st.text('검색하신 주식 종목이 없습니다. 정확하게 입력해주세요.')