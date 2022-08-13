from sklearn.svm import SVR
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import seaborn as sns
import koreanize_matplotlib

import datetime
import streamlit as st

start = datetime.datetime.now()-datetime.timedelta(days=94)
start = start.strftime('%Y-%m-%d')

stock_data = pdr.get_data_yahoo('000660.KS', start)

from sklearn.preprocessing import MinMaxScaler
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
print('RBF SVR : ', rbf_svr.predict(day))

predict = mms.inverse_transform(rbf_svr.predict(day).reshape(-1,1))

st.text(int(predict))