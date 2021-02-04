import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
from datetime import datetime
from datetime import timedelta
import yfinance as yf
import lxml as xml
from money import Money

st.title("Bitcoin Daily Analysis")

select_currency = st.sidebar.selectbox('Select currency?', ('BTC-GBP','BTC-USD'))
select_period = st.sidebar.selectbox('Select period?', ('10d','5d','1d'))
#select_interval = st.sidebar.selectbox('Select interval?', ('90m','60m','30m','15m','5m','2m','1m'))
select_interval = st.sidebar.selectbox('Select interval?', ('90m','60m','30m','15m','5m'))
select_window = st.sidebar.slider('Set window', min_value=10, max_value=50, value=20, step=5)
select_bollinger = st.sidebar.checkbox('Show bollonger bands?')
select_signals = st.sidebar.checkbox('Show signals?')
select_close = st.sidebar.checkbox('Show closing tracker?')

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

#fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
#               vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
#               row_width=[0.2, 0.7])
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Candlestick(x=btc_df['Datetime'],
            open=btc_df['Open'],
            high=btc_df['High'],
            low=btc_df['Low'],
            close=btc_df['Close'], name="OHLC"),
#              go.Scatter(x=btc_df.Datetime, y=btc_df.bollinger_mid_band, line=dict(color='orange', width=1), name='Mid'),
#              go.Scatter(x=btc_df.Datetime, y=btc_df.bollinger_upper_band, line=dict(color='red', width=1), name='Upper'),
#              go.Scatter(x=btc_df.Datetime, y=btc_df.bollinger_lower_band, line=dict(color='blue', width=1), name='Lower'), 
            secondary_y=True
)

fig.add_trace(go.Bar(x=btc_df.Datetime, y=btc_df.Volume, showlegend=False), secondary_y=False)

#fig.update(layout_xaxis_rangeslider_visible=False)
fig.layout.yaxis2.showgrid=False

if select_bollinger:
      fig.add_trace(go.Scatter(x=btc_df.Datetime, y=btc_df.bollinger_mid_band, line=dict(color='orange', width=1), name='Mid'))
      fig.add_trace(go.Scatter(x=btc_df.Datetime, y=btc_df.bollinger_upper_band, line=dict(color='red', width=1), name='Upper'))
      fig.add_trace(go.Scatter(x=btc_df.Datetime, y=btc_df.bollinger_lower_band, line=dict(color='blue', width=1), name='Lower'))

if select_signals:
      fig.add_trace(go.Scatter(x=btc_df.Datetime, y=btc_df.bollinger_signal, mode='markers', line=dict(color='black', width=1), name='Signal'))

if select_close:
      fig.add_trace(go.Scatter(x=btc_df.Datetime, y=btc_df.Close, line=dict(color='grey', width=1), name='Close'))
                    
fig

 
      
#fig = px.bar(btc_df, x="Datetime", y="Volume")

#fig

btc_df
