import streamlit as st
import numpy as np
import pandas as pd
from data.data import read_data
import pickle
import pathlib
from yahoo_fin import stock_info as si

minilist = ['A', 'ACN', 'VLO', 'AMC', 'GME', 'AAPL']
sp_list = si.tickers_sp500()
dow_list = si.tickers_dow()


def app():

    st.title('Testing data fetch/read')

    st.write("Should contain data from dowjones stocks at the moment")

    #st.markdown("### Plot Data")
    url = 'https://drive.google.com/file/d/1kg1cFbunr7qwoKm1QPYA38s0RnQd280W/view?usp=sharing'
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    df = pd.read_pickle(path)

    dividend = 'https://drive.google.com/file/d/150UDrwhVd3hH0nwU1Y0IptwlYIu5akR4/view?usp=sharing'
    divpath = 'https://drive.google.com/uc?export=download&id='+dividend.split('/')[-2]
    divdict = pd.read_pickle(divpath)
    Dividendslist = list(divdict.keys())

    newdf = read_data(Dividendslist)
    
    
    #st.dataframe(habadf)
    st.dataframe(newdf)
    
