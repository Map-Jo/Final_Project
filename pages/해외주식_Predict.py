import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import FinanceDataReader as fdr
from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense, Activation
import streamlit as st
import tensorflow 

st.set_page_config(
    page_title="반포자이까지 한걸음",
    page_icon= "chart_with_upwards_trend",
    layout="wide",
)

st.sidebar.markdown("# Predict Overseas_stocks 📊")

Stockcode = pd.read_csv('data/oversea_stockcode.csv')
Stockcode.set_index('Symbol', inplace=True)
Name = st.text_input('Code Name', 'ticker를 입력해주세요.')
Stockcode['ticker'] = Stockcode.index

Year = st.text_input('Year (기간을 오래 설정할수록 예측 정확성이 높아집니다.)','2020')
Code_name_list = Stockcode.index.tolist()

if Name in Code_name_list:
    code_num = Stockcode.at[Name, 'ticker'][0]
    df = fdr.DataReader(code_num)
    df = df.rename(columns={'Open':'시가', 'High':'고가','Low':'저가', 'Close':'종가', 'Volume':'거래량', 'Change':'전일대비'})

    high_prices = df['고가'].values
    low_prices = df['저가'].values
    mid_prices = (high_prices + low_prices) / 2

    seq_len = 50
    sequence_length = seq_len + 1
    result = []
    for index in range(len(mid_prices) - sequence_length):
        result.append(mid_prices[index: index + sequence_length])

    normalized_data = []
    for window in result:
        try:
            normalized_window = [((float(p) / float(window[0])) - 1) for p in window] #정규화시키려는 공식.
            normalized_data.append(normalized_window)
        except ZeroDivisionError:
            result = 0
    result = np.array(normalized_data)
    row = int(round(result.shape[0] * 0.9))
    train = result[:row, :]
    np.random.shuffle(train)
    
    x_train = train[:, :-1]
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    y_train = train[:, -1]

    x_test = result[row:, :-1]
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    y_test = result[row:, -1]


    with st.spinner('Predict...'):
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(50, 1)))
        model.add(LSTM(64, return_sequences=False))
        model.add(Dense(1, activation='linear'))
        model.compile(loss='mse', optimizer='rmsprop')
        model.summary()

    with st.spinner('Model Fitting...'):
        model.fit(x_train, y_train,
        validation_data=(x_test, y_test),
        batch_size=10,
        epochs=10)

    st.success('Done!')
    pred = model.predict(x_test)
    fig = plt.figure(facecolor='white', figsize=(20, 10))
    ax = fig.add_subplot(111)
    ax.plot(y_test, label='True')
    ax.plot(pred, label='Prediction')
    ax.legend()
    st.pyplot(fig)

elif Name not in Code_name_list:
    st.text('검색하신 주식 종목이 없습니다. 정확하게 입력해주세요.')
