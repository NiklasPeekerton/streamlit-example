import streamlit as st
from multiapp import MultiApp
from apps import home
from apps import sp
from apps import dj
from apps import data_test




#st.set_page_config(layout="wide")


apps = MultiApp()

# Add all your application here

apps.add_app("Home", home.app)
apps.add_app("S&P", sp.app)
apps.add_app("Dow Jones", dj.app)
apps.add_app("Data test", data_test.app)


# The main app
apps.run()

