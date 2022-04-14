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

dow_list = si.tickers_dow()

def app():
    st.title('Stonkotracker 3000')

    #st.write("This is a sample home page in the mutliapp.")
    #st.write("See `apps/home.py` to know how to use it.")
    #st.bar_chart(data=None, width=0, height=0, use_container_width=True)

    newdf = read_data(dow_list)
    st.bar_chart(newdf)
