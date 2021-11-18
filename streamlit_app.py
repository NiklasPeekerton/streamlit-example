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


# get list of Dow tickers

dow_list = si.tickers_dow()
#sp_list = si.tickers_sp500()

# et data in the current column for each stock's valuation table
dow_stats = {}
for ticker in dow_list:
    temp = si.get_stats_valuation(ticker)
    temp = temp.iloc[:,:2]
    temp.columns = ["Attribute", "Recent"]
 
    dow_stats[ticker] = temp
 
 
# combine all the stats valuation tables into a single data frame
combined_stats = pd.concat(dow_stats)
combined_stats = combined_stats.reset_index()
 
del combined_stats["level_1"]
 
# update column names
combined_stats.columns = ["Ticker", "Attribute", "Recent"]

# get P/E ratio for each stock

dow_pe = combined_stats[combined_stats.Attribute.str.contains("Trailing P/E")]
dow_pe


"""
# S&P 500 NCAV
These are stocks listed on S&P 500 with their NCAV:
"""

sp_list = si.tickers_sp500()
dow_list = si.tickers_dow()

sp_stats = {} 
BalanceSheets = {}

allstats = []

for ticker in dow_list:
    temp = si.get_quote_data(ticker)
    sheet = si.get_balance_sheet(ticker)
    sp_stats[ticker] = temp
    BalanceSheets[ticker] = sheet


    try:
        allstats.append([ticker, BalanceSheets[ticker].loc['totalLiab'][0], BalanceSheets[ticker].loc['totalCurrentAssets'][0],
                        sp_stats[ticker]['regularMarketPrice'], sp_stats[ticker]['sharesOutstanding']])
    except:
        print(ticker)


allstatsdf = pd.DataFrame(allstats, columns=['Ticker','TotalLiabilities','CurrentAssets','Market Price', 'Shares Outstanding'])
allstatsdf

