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

dow_list = si.tickers_dow()

def app():
    st.title('Stonkotracker 3000')

    #st.write("This is a sample home page in the mutliapp.")
    #st.write("See `apps/home.py` to know how to use it.")
    #st.bar_chart(data=None, width=0, height=0, use_container_width=True)
    dividend = 'https://drive.google.com/file/d/150UDrwhVd3hH0nwU1Y0IptwlYIu5akR4/view?usp=sharing'
    divpath = 'https://drive.google.com/uc?export=download&id='+dividend.split('/')[-2]
    divdict = pd.read_pickle(divpath)
    Dividendslist = list(divdict.keys())

    newdf = read_data(Dividendslist)
    overall = newdf[['Ticker','Name','Overall score']].sort_values(by=['Overall score'], ascending=False)
    c = alt.Chart(overall).mark_circle().encode(
     x='Name', y='Overall score', size='Overall score', color='Overall score', tooltip=['Name', 'Overall score'])

    st.altair_chart(c, use_container_width=True)
