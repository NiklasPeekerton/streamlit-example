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
    dow = fetch_data(dow_list)
    #sp = fetch_data(sp_list)
    clickdow = st.button('Fetch data', key='1')
    if clickdow:
        dow
        st.write('Downloading data')
    #clicksp = st.button('Fetch data', key='2')
    #if clicksp:
    #    sp
    #    st.write('Downloading data')
    

    #st.line_chart(df)
    #clicks = st.button('Fetch data', key='1')
    newdf = fetch_data(minilist)

    
    
    
    st.dataframe(newdf)
    
    st.write("Does it get this far")
