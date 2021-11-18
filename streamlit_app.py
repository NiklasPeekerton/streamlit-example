from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# überStocks

"""


"""
# Dow Jones PE values
These are stocks listed on Dow Jones sorted by PE:
"""

import pandas as pd
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

from yahoo_fin import stock_info as si

@st.cache
# get list of Dow tickers
dow_list = si.tickers_dow()
#sp_list = si.tickers_sp500()
 @st.cache
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
