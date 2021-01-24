# Import libraries and dependencies
import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import warnings
from datetime import datetime
from datetime import timedelta
import yfinance as yf
import lxml as xml
from money import Money

st.title("Bitcoin Daily Analysis")

select_currency = st.sidebar.selectbox('Select currency?', ('BTC-GBP','BTC-USD'))
select_period = st.sidebar.selectbox('Select period?', ('1d','5d','10d'))
select_interval = st.sidebar.selectbox('Select interval?', ('1m','2m','5m','15m','30m','60m','90m'))
select_window = st.sidebar.slider('Window', min_value=1, max_value=50, value=10, step=1)
select_signals = st.sidebar.checkbox('Signals?')

btc_df = yf.download(tickers=select_currency, period=select_period, interval=select_interval)

btc_df = btc_df.reset_index()
for i in ['Open', 'High', 'Close', 'Low']: 
      btc_df[i]  =  btc_df[i].astype('float64')

#bollinger_window = 10
btc_df['bollinger_mid_band'] = btc_df['Close'].rolling(window=select_window).mean()
btc_df['bollinger_std'] = btc_df['Close'].rolling(window=select_window).std()
btc_df['bollinger_upper_band']  = btc_df['bollinger_mid_band'] + (btc_df['bollinger_std'] * 1)
btc_df['bollinger_lower_band']  = btc_df['bollinger_mid_band'] - (btc_df['bollinger_std'] * 1)
btc_df['bollinger_long'] = np.where(btc_df['Close'] < btc_df['bollinger_lower_band'], 1.0, 0.0)
btc_df['bollinger_short'] = np.where(btc_df['Close'] > btc_df['bollinger_upper_band'], -1.0, 0.0)

btc_df['bollinger_signal'] = np.where(btc_df['bollinger_long'] + btc_df['bollinger_short'] > 0, btc_df['Close'], None)

mc = yf.Ticker(select_currency)
cur = select_currency
cur = cur[-3:]
st.write("Market capitalisation: " + str(Money(mc.info["marketCap"], cur)))
st.write("Bollinger band window:" + str(select_window))

fig = go.Figure(data=[go.Candlestick(x=btc_df['Datetime'],
            open=btc_df['Open'],
            high=btc_df['High'],
            low=btc_df['Low'],
            close=btc_df['Close']), 
              go.Scatter(x=btc_df.Datetime, y=btc_df.Close, line=dict(color='grey', width=1), name='Close'),
              go.Scatter(x=btc_df.Datetime, y=btc_df.bollinger_mid_band, line=dict(color='orange', width=1), name='Mid'),
              go.Scatter(x=btc_df.Datetime, y=btc_df.bollinger_upper_band, line=dict(color='red', width=1), name='Upper'),
              go.Scatter(x=btc_df.Datetime, y=btc_df.bollinger_lower_band, line=dict(color='blue', width=1), name='Lower')
                     ])
if select_signals:
      fig.add_trace(go.Scatter(x=btc_df.Datetime, y=btc_df.bollinger_signal, mode='markers', line=dict(color='black', width=1), name='Signal'))

fig


fig = px.bar(btc_df, x="Datetime", y="Volume")
fig

btc_df
