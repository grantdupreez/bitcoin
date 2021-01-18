# Import libraries and dependencies
import pandas as pd
import streamlit as st
import numpy as np
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import warnings
import requests
#import html5lib
from datetime import datetime
from dateutil.relativedelta import relativedelta
import lxml.html
from typing import Dict, List

#collect data

def get_start_date(number_of_months:int):
    now = datetime.now()
    dt_end = now.strftime("%Y%m%d")
    dt_start = (now - relativedelta(months=number_of_months)).strftime("%Y%m%d")
    return dt_start

def coinmarketcap_get_btc(start_date: str, end_date: str) -> List[Dict]:
    # Build the url
    url = f'https://coinmarketcap.com/currencies/bitcoin/historical-data/?start={start_date}&end={end_date}'
    # Make the request and parse the tree
    response = requests.get(url, timeout=5)
    tree = lxml.html.fromstring(response.text)
    # Extract table and raw data
    table = tree.find_class('cmc-table')[0]
    xpath_0, xpath_1 = 'div[3]/div/table/thead/tr', 'div[3]/div/table/tbody/tr/td[%d]/div'
    cols = [_.text_content() for _ in table.xpath(xpath_0 + '/th')]
    dates = (_.text_content() for _ in table.xpath(xpath_1 % 1))
    m = map(lambda d: (float(_.text_content().replace(',', '')) for _ in table.xpath(xpath_1 % d)),
            range(2, 8))
    return [{k: v for k, v in zip(cols, _)} for _ in zip(dates, *m)]

############
number_of_months = 3

coinmarketcap_get_btc(get_start_date(3), now.strftime("%Y%m%d"))

warnings.filterwarnings('ignore')
# Set path to CSV and read in CSV
csv_path = Path('sample_data.csv')
btc_df=pd.read_csv(csv_path)
btc_df.head()

# Set index as datetime object and drop columns
btc_df.set_index(pd.to_datetime(btc_df['Timestamp'], infer_datetime_format=True), inplace=True)
#btc_df.drop(columns=['Timestamp'], inplace=True)
btc_df.head()

# Drop NAs and calculate daily percent return
btc_df['daily_return'] = btc_df['Close'].dropna().pct_change()
btc_df

# Set short and long windows
short_window = 1
long_window = 10
# Construct a `Fast` and `Slow` Exponential Moving Average from short and long windows, respectively
btc_df['fast_close'] = btc_df['Close'].ewm(halflife=short_window).mean()
btc_df['slow_close'] = btc_df['Close'].ewm(halflife=long_window).mean()
# Construct a crossover trading signal
btc_df['crossover_long'] = np.where(btc_df['fast_close'] > btc_df['slow_close'], 1.0, 0.0)
btc_df['crossover_short'] = np.where(btc_df['fast_close'] < btc_df['slow_close'], -1.0, 0.0)
btc_df['crossover_signal'] = btc_df['crossover_long'] + btc_df['crossover_short']
btc_df.head()
st.write("Set short and long windows")
btc_df


# Set bollinger band window
bollinger_window = 20
# Calculate rolling mean and standard deviation
btc_df['bollinger_mid_band'] = btc_df['Close'].rolling(window=bollinger_window).mean()
btc_df['bollinger_std'] = btc_df['Close'].rolling(window=20).std()
# Calculate upper and lowers bands of bollinger band
btc_df['bollinger_upper_band']  = btc_df['bollinger_mid_band'] + (btc_df['bollinger_std'] * 1)
btc_df['bollinger_lower_band']  = btc_df['bollinger_mid_band'] - (btc_df['bollinger_std'] * 1)
# Calculate bollinger band trading signal
btc_df['bollinger_long'] = np.where(btc_df['Close'] < btc_df['bollinger_lower_band'], 1.0, 0.0)
btc_df['bollinger_short'] = np.where(btc_df['Close'] > btc_df['bollinger_upper_band'], -1.0, 0.0)
btc_df['bollinger_signal'] = btc_df['bollinger_long'] + btc_df['bollinger_short']
st.write("Set bollinger band window")
btc_df

# Plot 
fig = go.Figure(data=[go.Candlestick(x=btc_df['Timestamp'],
                open=btc_df['Open'],
                high=btc_df['High'],
                low=btc_df['Low'],
                close=btc_df['Close']), 
                  go.Scatter(x=btc_df.Timestamp, y=btc_df.Close, line=dict(color='orange', width=1)),
                  go.Scatter(x=btc_df.Timestamp, y=btc_df.bollinger_mid_band, line=dict(color='green', width=1)),
                  go.Scatter(x=btc_df.Timestamp, y=btc_df.bollinger_upper_band, line=dict(color='red', width=1)),
                  go.Scatter(x=btc_df.Timestamp, y=btc_df.bollinger_lower_band, line=dict(color='blue', width=1))
            ])
fig
