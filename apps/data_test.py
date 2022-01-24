import streamlit as st
import numpy as np
import pandas as pd
from data.data import fetch_data
import pickle
import pathlib

minilist = ['A', 'ACN']



def app():

    st.title('Testing data fetch/read')

    st.write("Should contain data from 2 stocks at the moment")

    #st.markdown("### Plot Data")
    #df = fetch_data()

    #st.line_chart(df)
    clicks = st.button('Fetch data', key='1')

    if clicks:
        fetch_data()
        st.write('Downloading data')
    
    st.dataframe(habadf)
    
    st.write("Does it get this far")
