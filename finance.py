import pandas as pd
import streamlit as st
import FinanceDataReader as fdr


code = st.text_input('Code Num')
date = st.number_input('Date')
df = fdr.DataReader(code, date)
df
