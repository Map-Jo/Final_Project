import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="반포자이까지 한걸음",
    page_icon= "chart_with_upwards_trend",
    # layout="wide", 
)

st.title('업종별 종목입니다.')
# st.sidebar.markdown("# 업종명 📊")

sector = pd.read_csv('data/sector.csv')

sector_list = list(sector['업종명'].unique())
choice = st.sidebar.selectbox('업종명',sector_list)

for i in range(0, 70) :
    if choice == sector_list[i] :
      st.table(sector['종목명'].loc[sector['업종명']==sector_list[i]])
