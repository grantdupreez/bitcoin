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

#warnings.filterwarnings('ignore')

btc_df

fig = go.Figure(data=[go.Candlestick(x=btc_df['Datetime'],
            open=btc_df['Open'],
            high=btc_df['High'],
            low=btc_df['Low'],
            close=btc_df['Close']), 
              go.Scatter(x=btc_df.Datetime, y=btc_df.Close, line=dict(color='orange', width=1), name='Close')
        ])

fig
