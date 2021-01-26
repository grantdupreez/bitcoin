import yfinance as yf
from pandas_datareader import data as pdr

yf.pdr_override()
#bc = yf.Ticker("BTC-GBP")
#df = yf.download("BTC-GBP", start="2017-01-01", end="2021-01-26")
df = pdr.get_data_yahoo("BTC-GBP", start="2021-01-18", end="2021-01-26")
df
