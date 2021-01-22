# Import libraries and dependencies
import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import warnings
from datetime import datetime
from datetime import timedelta
import yfinance as yf
import lxml as xml
from money import Money

st.title("Bitcoin Daily Analysis")

bc = 'BTC-GBP'

select_period = st.sidebar.selectbox('What period?', ('1d','5d','1mo'))
select_interval = st.sidebar.selectbox('What interval?', ('1m','2m','5m','15m','30m','60m','90m','1h'))


btc_df = yf.download(tickers=bc, period=select_period, interval=select_interval)

btc_df = btc_df.reset_index()
for i in ['Open', 'High', 'Close', 'Low']: 
      btc_df[i]  =  btc_df[i].astype('float64')

bollinger_window = 10
btc_df['bollinger_mid_band'] = btc_df['Close'].rolling(window=bollinger_window).mean()
btc_df['bollinger_std'] = btc_df['Close'].rolling(window=bollinger_window).std()
btc_df['bollinger_upper_band']  = btc_df['bollinger_mid_band'] + (btc_df['bollinger_std'] * 1)
btc_df['bollinger_lower_band']  = btc_df['bollinger_mid_band'] - (btc_df['bollinger_std'] * 1)
btc_df['bollinger_long'] = np.where(btc_df['Close'] < btc_df['bollinger_lower_band'], 1.0, 0.0)
btc_df['bollinger_short'] = np.where(btc_df['Close'] > btc_df['bollinger_upper_band'], -1.0, 0.0)
btc_df['bollinger_signal'] = btc_df['bollinger_long'] + btc_df['bollinger_short']
st.write("Set bollinger band window - window:" + str(bollinger_window))

btc_df

fig = go.Figure(data=[go.Candlestick(x=btc_df['Datetime'],
            open=btc_df['Open'],
            high=btc_df['High'],
            low=btc_df['Low'],
            close=btc_df['Close']), 
              go.Scatter(x=btc_df.Datetime, y=btc_df.Close, line=dict(color='orange', width=1), name='Close'),
              go.Scatter(x=btc_df.Datetime, y=btc_df.bollinger_mid_band, line=dict(color='green', width=1), name='Mid'),
              go.Scatter(x=btc_df.Datetime, y=btc_df.bollinger_upper_band, line=dict(color='red', width=1), name='Upper'),
              go.Scatter(x=btc_df.Datetime, y=btc_df.bollinger_lower_band, line=dict(color='blue', width=1), name='Lower')])

fig
