import streamlit as st
import pandas as pd
import base64
from bs4 import BeautifulSoup
import requests
import json
import time

@st.cache
def load_data():
    url = "https://coinmarketcap.com/currencies/bitcoin/historical-data/?start="
    start_date = "20210101&end="
    end_date = "20210113"
    cmc = requests.get(url + start_date + end_date)
    soup = BeautifulSoup(cmc.content, 'html.parser')
    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    historical_data = json.loads(data.contents[0])
    quotes = historical_data['props']['initialState']['cryptocurrency']['ohlcvHistorical']['quotes']
#    listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']


    market_cap = []
    volume = []
    timestamp = []
    coin_name = []
    coin_symbol = []
    price = []

    for i in quotes:
      coin_name.append(info['name'])
      coin_symbol.append(info['symbol'])
      market_cap.append(i['quote'][GBP]['market_cap'])
      volume.append(i['quote'][GBP]['volume_24h'])
      price.append(i['quote']['GBP']['price'])
      timestamp.append(i['quote'][GBP]['timestamp'])
    

    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap', 'volume', 'price', 'timestamp'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['market_cap'] = market_cap
    df['volume'] = volume
    df['timestamp'] = timestamp
    return df

df = load_data()

st.write(df)
