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


dow_list = si.tickers_dow()

sp_stats = {} 


@st.cache
def get_data():
    for ticker in dow_list:
        temp = si.get_quote_data(ticker)
        sp_stats[ticker] = temp
     
    return sp_stats

df = get_data()
df


