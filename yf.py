import yfinance as yf

bc = yf.Ticker("BTC-GBP")
df = yf.download("BTC-GBP", start="2017-01-01", end="2021-01-26")
df
