import pandas as pd
import streamlit as st
import numpy as np
import warnings
from datetime import datetime
from datetime import timedelta
import yfinance as yf
import lxml as xml
from money import Money
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import Activation
from keras.models import load_model

st.title("Bitcoin Hourly Predition")

select_currency = st.sidebar.selectbox('Select currency?', ('BTC-GBP','BTC-USD'))
select_period = st.sidebar.selectbox('Select period?', ('10d','5d','1d'))
select_interval = st.sidebar.selectbox('Select interval?', ('90m','60m','30m','15m','5m','2m','1m'))

df = yf.download(tickers=select_currency, period=select_period, interval=select_interval)

