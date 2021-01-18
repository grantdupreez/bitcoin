# Import libraries and dependencies
import pandas as pd
import streamlit as st
import numpy as np
from pathlib import Path
import plotly.graph_objects as go
import warnings

warnings.filterwarnings('ignore')
# Set path to CSV and read in CSV
csv_path = Path('sample_data.csv')
btc_df=pd.read_csv(csv_path)
btc_df.head()

# Set index as datetime object and drop columns
btc_df.set_index(pd.to_datetime(btc_df['Timestamp'], infer_datetime_format=True), inplace=True)
btc_df.drop(columns=['Timestamp'], inplace=True)
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

# Plot the Bollinger Bands for BTC/USD closing prices
#fig = px.line(btc_df[['Close','bollinger_mid_band','bollinger_upper_band','bollinger_lower_band']])
#fig.show()
fig = go.Figure([go.Scatter(x=btc_df['Timestamp'], y=btc_df[['Close','bollinger_mid_band','bollinger_upper_band','bollinger_lower_band']])])
fig
