import requests
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_date_range(number_of_months:int):
    now = datetime.now()
    dt_end = now.strftime("%Y%m%d")
    dt_start = (now - relativedelta(months=number_of_months)).strftime("%Y%m%d")
    return f'start={dt_start}&end={dt_end}'

number_of_months = 3

table = pd.read_html(f'https://coinmarketcap.com/currencies/bitcoin/historical-data/?{get_date_range(number_of_months)}')[0]
table = table[['Date', 'Close**', 'Volume','Market Cap']]
print(table)
