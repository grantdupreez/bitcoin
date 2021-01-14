import pandas
import requests
from bs4 import BeautifulSoup

link = 'https://coinmarketcap.com/currencies/bitcoin/historical-data/?start={}&end={}'

def get_coinmarketcap_info(url,s_date,e_date):
    response = requests.get(url.format(s_date,e_date))
    soup = BeautifulSoup(response.text,"lxml")

    for items in soup.select("table.table tr.text-right"):
        date = items.select_one("td.text-left").get_text(strip=True)
        close = items.select_one("td[data-format-market-cap]").find_previous_sibling().get_text(strip=True)
        volume = items.select_one("td[data-format-market-cap]").get_text(strip=True)
        marketcap = items.select_one("td[data-format-market-cap]").find_next_sibling().get_text(strip=True)
        yield date,close,volume,marketcap

if __name__ == '__main__':
    dataframe = (elem for elem in get_coinmarketcap_info(link,s_date='20210101',e_date='20210113'))
    df = pandas.DataFrame(dataframe)
    print(df)
