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

    st.write(quotes)
