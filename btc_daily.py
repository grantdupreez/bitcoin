# Import libraries and dependencies
import pandas as pd
import streamlit as st
import numpy as np
import hvplot.pandas
import warnings
from datetime import datetime
import yfinance as yf
import lxml as xml
from money import Money

st.title("Bitcoin Daily Analysis")

bc = 'BTC-GBP'
y_data = yf.Ticker(bc)

today = datetime.today()
st_date = today - timedelta(days=1)
start_date = st.sidebar.date_input("Start Date", st_date)
to_date = f'{datetime.now():%Y-%m-%d}'

btc_df = y_data.download(bc, start=start_date, end=to_date, interval="1d")


btc_df = btc_df.reset_index()
for i in ['Open', 'High', 'Close', 'Low']: 
      btc_df[i]  =  btc_df[i].astype('float64')

warnings.filterwarnings('ignore')

# Set index as datetime object and drop columns
btc_df.set_index(pd.to_datetime(btc_df['Date'], infer_datetime_format=True), inplace=True)
btc_df.head()

# Drop NAs and calculate daily percent return
btc_df['daily_return'] = btc_df['Close'].dropna().pct_change()
#btc_df

signals_df = btc_df.drop(columns=['Open', 'High', 'Low', 'Volume','Dividends', 'Stock Splits'])

# Set the short window and long windows
short_window = 50
long_window = 100
# Generate the short and long moving averages (50 and 100 days, respectively)
signals_df['SMA50'] = signals_df['Close'].rolling(window=short_window).mean()
signals_df['SMA100'] = signals_df['Close'].rolling(window=long_window).mean()
signals_df['Signal'] = 0.0
# Generate the trading signal 0 or 1,
# where 0 is when the SMA50 is under the SMA100, and
# where 1 is when the SMA50 is higher (or crosses over) the SMA100
signals_df['Signal'][short_window:] = np.where(
    signals_df['SMA50'][short_window:] > signals_df['SMA100'][short_window:], 1.0, 0.0
)
# Calculate the points in time at which a position should be taken, 1 or -1
signals_df['Entry/Exit'] = signals_df['Signal'].diff()
# Print the DataFrame
signals_df.tail(10)

# Visualize exit position relative to close price
exit = signals_df[signals_df['Entry/Exit'] == -1.0]['Close'].hvplot.scatter(
    color='red',
    legend=False,
    ylabel='Price in $',
    width=1000,
    height=400
)
# Visualize entry position relative to close price
entry = signals_df[signals_df['Entry/Exit'] == 1.0]['Close'].hvplot.scatter(
    color='green',
    legend=False,
    ylabel='Price in $',
    width=1000,
    height=400
)
# Visualize close price for the investment
security_close = signals_df[['Close']].hvplot(
    line_color='lightgray',
    ylabel='Price in $',
    width=1000,
    height=400
)
# Visualize moving averages
moving_avgs = signals_df[['SMA50', 'SMA100']].hvplot(
    ylabel='Price in $',
    width=1000,
    height=400
)
# Overlay plots
entry_exit_plot = security_close * moving_avgs * entry * exit
entry_exit_plot.opts(xaxis=None)
