import yfinance as yf

btc = yf.Ticker("BTC-GBP")
btc.history(period="max")
btc
