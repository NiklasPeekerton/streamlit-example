import streamlit as st
from multiapp import MultiApp
from apps import home
from apps import sp
from apps import dj
from apps import data_test
from apps import Russell3000
from apps import nasdaq
from apps import ftse100
from apps import ftse250
from apps import nifty50
from apps import niftybank
from apps import ibovespa



#st.set_page_config(layout="wide")


apps = MultiApp()

# Add all your application here

apps.add_app("Home", home.app)
apps.add_app("S&P", sp.app)
apps.add_app("Dow Jones", dj.app)
apps.add_app("Russell3000", Russell3000.app)
apps.add_app("Nasdaq", nasdaq.app)
apps.add_app("FTSE 100", ftse100.app)
apps.add_app("FTSE 250", ftse250.app)
apps.add_app("NIFTY 50", nifty50.app)
apps.add_app("NIFTY bank", niftybank.app)
apps.add_app("IBOVESPA", ibovespa.app)
apps.add_app("Data test", data_test.app)


# The main app
apps.run()

