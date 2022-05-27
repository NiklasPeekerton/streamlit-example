import streamlit as st
import pandas as pd
import numpy as np
from apps import dj
from yahoo_fin import stock_info as si
from tqdm.notebook import trange, tqdm
import pickle
import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
from data.data import read_data
import altair as alt
import plotly.tools

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

    newdf = read_data(Dividendslist, Dividendslist)
    
    
    #st.dataframe(habadf)
    st.dataframe(newdf)
    
