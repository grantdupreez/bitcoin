import yfinance as yf

bc = yf.Ticker("BTC-GBP")
df = bc.history(period="max")
df
