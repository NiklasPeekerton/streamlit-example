import pandas as pd
import numpy as np
from yahoo_fin import stock_info as si
from tqdm.notebook import trange, tqdm
import pickle
import streamlit as st
from datetime import datetime
import streamlit as st
from streamlit_option_menu import option_menu

#with st.sidebar:
#    selected = option_menu("Main Menu", ["Home", 'Settings'], 
#        icons=['house', 'gear'], menu_icon="cast", default_index=1)
#    selected

# horizontal menu
#selected2 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'], 
#    icons=['house', 'cloud-upload', "list-task", 'gear'], 
#    menu_icon="cast", default_index=0, orientation="horizontal")
#selected2


sp_list = si.tickers_sp500()
dow_list = si.tickers_dow()
minilist = ['A', 'ACN']

Financials = {}
Quote = {}
Dividends = {}
Earnings = {}
Price = {}

def fetch_data():
    for ticker in tqdm(minilist):
        try:
            fin = si.get_financials(ticker, yearly=True, quarterly=False)
            qut = si.get_quote_data(ticker)
            div = si.get_dividends(ticker)
            earn = si.get_earnings_history(ticker)
            price = si.get_data(ticker,interval='1mo')
            Financials[ticker] = fin
            Quote[ticker] = qut
            Dividends[ticker] = div
            Earnings[ticker] = earn
            Price[ticker] = price
        except Exception as e:
            print(ticker, e, 'contains sum bullshit')

    with open('Financials.pkl', 'wb') as f:
        pickle.dump(Financials, f)

    with open('Quote.pkl', 'wb') as f:
        pickle.dump(Quote, f)

    with open('Dividends.pkl', 'wb') as f:
        pickle.dump(Dividends, f)

    with open('Earnings.pkl', 'wb') as f:
        pickle.dump(Earnings, f)

    with open('Price.pkl', 'wb') as f:
        pickle.dump(Price, f)

    return()
