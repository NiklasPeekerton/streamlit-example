from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from yahoo_fin import stock_info as si

"""
# überStocks

"""


"""
# Dow Jones PE values
These are stocks listed on Dow Jones sorted by PE:
"""



"""
# S&P 500 NCAV
These are stocks listed on S&P 500 with their NCAV:
"""


sp_list = si.tickers_sp500()
dow_list = si.tickers_dow()

sp_stats = {} 
BalanceSheets = {}

allstats = []

@st.cache
def get_data():
    for ticker in dow_list:
        temp = si.get_quote_data(ticker)
        sheet = si.get_balance_sheet(ticker)
        sp_stats[ticker] = temp
        BalanceSheets[ticker] = sheet
     
    return sp_stats

df = get_data()

for ticker in dow_list:
    try:
        allstats.append([ticker, BalanceSheets[ticker].loc['totalLiab'][0], BalanceSheets[ticker].loc['totalCurrentAssets'][0],
                        sp_stats[ticker]['regularMarketPrice'], sp_stats[ticker]['sharesOutstanding']])
    except:
        print(ticker)

allstats


