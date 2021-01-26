import yfinance as yf

btc = yf.Ticker("BTC-GBP")
df = btc.history(period="max")
df
