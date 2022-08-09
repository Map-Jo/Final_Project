import pandas as pd
import streamlit as st
import FinanceDataReader as fdr


code = st.text_input('Code Num')
date = st.date_input(
     "When's your birthday",
     datetime.date(2019, 7, 6))
df = fdr.DataReader(code, date).sort_index(ascending=False)
df
