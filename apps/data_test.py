import streamlit as st
import numpy as np
import pandas as pd
from data.data import fetch_data
import pickle
import pathlib

minilist = ['A', 'ACN']



def app():

    st.title('Testing data fetch/read')

    st.write("Should contain data from dowjones stocks at the moment")

    #st.markdown("### Plot Data")
    #df = fetch_data()

    #st.line_chart(df)
    #clicks = st.button('Fetch data', key='1')
    newdf = fetch_data(dow_list)

    #if clicks:
        #newdf = fetch_data()
        #newdf
        #st.write('Downloading data')
    
    st.dataframe(newdf)
    
    st.write("Does it get this far")
