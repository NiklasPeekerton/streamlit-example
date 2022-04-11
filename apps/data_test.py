import streamlit as st
import numpy as np
import pandas as pd
from data.data import fetch_data
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

    apple = df['AAPL']
    
    
    st.dataframe(apple)
    
    st.write("Does it get this far")
