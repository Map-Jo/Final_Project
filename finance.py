import pandas as pd
import streamlit as st
import FinanceDataReader as fdr

Stockcode = pd.read_csv('data/Stockcode.csv')
Stockcode.set_index('Name', inplace=True)
Code_name_list = Stockcode.index.tolist()

if Name in Code_name_list:
    Name = st.text_input('Code Name','종목명을 입력하세요.')
    code_num = Stockcode.at[Name, 'Symbol']
    df = fdr.DataReader(code_num)
    df = df.rename(columns={'Open':'시가', 'High':'고가','Low':'저가', 'Close':'종가', 'Volume':'거래량', 'Change':'전일대비'})
else:
    pass

col1, col2, col3 = st.columns(3)
col1.metric("현재 주식가격","%d원" %df['종가'].tail(1)[0], "%d원" %df['종가'].diff().tail(1)[0])
col2.metric("현재 거래량", df['거래량'].tail(1)[0],"%.2f%%" %(df['거래량'].pct_change().tail(1)[0] * 100))
col3.metric("전일 대비 가격", round(df['전일대비'].tail(1)[0], 4), "%.2f%%" %(df['전일대비'].tail(1)[0] * 100))

