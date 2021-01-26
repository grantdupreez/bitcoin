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
from pandas_datareader import data as pdr

st.title("Bitcoin Market Analysis")

selected_ma = st.sidebar.slider('Moving average', min_value=10, max_value=100, value=50, step=10)

uploaded_file = st.sidebar.file_uploader("Choose a file",type=['CSV'])
if uploaded_file is not None:
    btc_df = pd.read_csv(uploaded_file, header=[0])
    btc_df.head()

    warnings.filterwarnings('ignore')

    # Set index as datetime object and drop columns
    btc_df.set_index(pd.to_datetime(btc_df['Date'], infer_datetime_format=True), inplace=True)
    btc_df.head()

    # Drop NAs and calculate daily percent return
    btc_df['daily_return'] = btc_df['Close'].dropna().pct_change()
    #btc_df

    # Set short and long windows
    short_window = 10
    long_window = selected_ma
    st.write("Short window set to: 10 / Long window set to: " + str(selected_ma))
    # Construct a `Fast` and `Slow` Exponential Moving Average from short and long windows, respectively
    btc_df['fast_close'] = btc_df['Close'].ewm(halflife=short_window).mean()
    btc_df['slow_close'] = btc_df['Close'].ewm(halflife=long_window).mean()
    btc_df['signal'] = np.where(btc_df['fast_close'] > btc_df['slow_close'], btc_df['Close'], None)
    btc_df.head()

    st.write("Exponential Moving Average (EMA) of Closing prices")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=btc_df.Date, y=btc_df['Close'],
                  mode='lines',
                  name='Close'))
    fig.add_trace(go.Scatter(x=btc_df.Date, y=btc_df.fast_close,
                  mode='lines',
                  name='SMA = 10'))
    fig.add_trace(go.Scatter(x=btc_df.Date, y=btc_df.slow_close,
                  mode='lines',
                  name='SMA = ' + str(selected_ma)))
    if btc_df['signal'] is not None:
            fig.add_trace(go.Scatter(x=btc_df.Date, y=btc_df['Close'],
                  mode='markers',
                  name='Signal'))

    fig

    st.write("EMA of Daily Return Volatility")
    st.write("EMA of the closing prices represents a moving average with more weight on the most recent of prices")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=btc_df.Date, y=btc_df['slow_close'],
                  mode='lines',
                  name='Slow Close'))
    fig.add_trace(go.Scatter(x=btc_df.Date, y=btc_df.fast_close,
                  mode='lines',
                  name='Fast Close'))
    fig


    # Set bollinger band window
    bollinger_window = selected_ma
    # Calculate rolling mean and standard deviation
    btc_df['bollinger_mid_band'] = btc_df['Close'].rolling(window=bollinger_window).mean()
    btc_df['bollinger_std'] = btc_df['Close'].rolling(window=selected_ma).std()
    # Calculate upper and lowers bands of bollinger band
    btc_df['bollinger_upper_band']  = btc_df['bollinger_mid_band'] + (btc_df['bollinger_std'] * 1)
    btc_df['bollinger_lower_band']  = btc_df['bollinger_mid_band'] - (btc_df['bollinger_std'] * 1)
    # Calculate bollinger band trading signal
    btc_df['bollinger_long'] = np.where(btc_df['Close'] < btc_df['bollinger_lower_band'], 1.0, 0.0)
    btc_df['bollinger_short'] = np.where(btc_df['Close'] > btc_df['bollinger_upper_band'], -1.0, 0.0)
    btc_df['bollinger_signal'] = btc_df['bollinger_long'] + btc_df['bollinger_short']
    st.write("Set bollinger band window - window: " + str(selected_ma))

    # Plot  
    st.write("Bollinger Bands")

    fig = go.Figure(data=[go.Candlestick(x=btc_df['Date'],
              open=btc_df['Open'],
              high=btc_df['High'],
              low=btc_df['Low'],
              close=btc_df['Close']), 
                go.Scatter(x=btc_df.Date, y=btc_df.Close, line=dict(color='orange', width=1), name='Close'),
                go.Scatter(x=btc_df.Date, y=btc_df.bollinger_mid_band, line=dict(color='green', width=1), name='Mid'),
                go.Scatter(x=btc_df.Date, y=btc_df.bollinger_upper_band, line=dict(color='red', width=1), name='Upper'),
                go.Scatter(x=btc_df.Date, y=btc_df.bollinger_lower_band, line=dict(color='blue', width=1), name='Lower'),
          ])
    fig
    
    st.write("Volume")
    fig = px.bar(btc_df, x="Date", y="Volume")
    fig
