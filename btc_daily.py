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

y_data = yf.Ticker(bc)

today = datetime.today()
st_date = today - timedelta(days=2)
start_date = st.sidebar.date_input("Start Date", st_date)
to_date = f'{datetime.now():%Y-%m-%d}'

btc_df = y_data.history(bc, start=start_date, end=to_date, interval="1h")


btc_df = btc_df.reset_index()
for i in ['Open', 'High', 'Close', 'Low']: 
      btc_df[i]  =  btc_df[i].astype('float64')

warnings.filterwarnings('ignore')

# Set index as datetime object and drop columns
btc_df.set_index(pd.to_datetime(btc_df['Date'], infer_datetime_format=True), inplace=True)
btc_df.head()

# Drop NAs and calculate daily percent return
btc_df['daily_return'] = btc_df['Close'].dropna().pct_change()

btc_df



fig = go.Figure(data=[go.Candlestick(x=btc_df['Date'],
            open=btc_df['Open'],
            high=btc_df['High'],
            low=btc_df['Low'],
            close=btc_df['Close']), 
              go.Scatter(x=btc_df.Date, y=btc_df.Close, line=dict(color='orange', width=1), name='Close')
        ])

fig
