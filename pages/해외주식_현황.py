# 환율 변환 코드출처: https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=nanayagoon&logNo=221246948133

import pandas as pd
import streamlit as st
import FinanceDataReader as fdr
import urllib.request

st.set_page_config(
    page_title="반포자이까지 한걸음",
    page_icon= "chart_with_upwards_trend",
    layout="wide",
)

st.sidebar.markdown("# Overseas Stocks 📊")

st.title('Overseas Stocks 📈')


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
Name = st.text_input('Code Name', 'ticker를 입력해주세요.')
Code_name_list = Stockcode.index.tolist()
Stockcode['ticker'] = Stockcode.index
if Name in Code_name_list:
    code_num = Stockcode.at[Name, 'ticker']
    df = fdr.DataReader(code_num)
    money = df['Close'].tail(1)
    k_money = float(money)*float(usdletter)
    k_money = round(k_money,2)
    k_money = format(k_money, ',')

    col1, col2, col3 = st.columns(3)
    col1.metric("현재 주식가격",format(df['Close'].tail(1)[0], ',')+'$', "%s원" %k_money)
    col2.metric("현재 거래량", format(round(df['Volume'].tail(1)[0]), ','),"%.2f%%" %(df['Volume'].pct_change().tail(1)[0] * 100))
    col3.metric("전일 대비 가격", "%d$" %(df['Close'].diff().tail(1)[0]), "%.2f%%" %(df['Change'].tail(1)[0] * 100))
    st.text(prin +'의 KEB하나은행 환율정보 입니다.')
    st.text('현재 1$당 '+str(usdletter)+'원 입니다.')
elif Name not in Code_name_list:
    st.text('검색하신 주식 종목이 없습니다. 정확하게 입력해주세요.')
