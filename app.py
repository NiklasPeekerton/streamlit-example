import streamlit as st
from multiapp import MultiApp
from apps import home
from apps import sp
from apps import dj




#st.set_page_config(layout="wide")


apps = MultiApp()

# Add all your application here

apps.add_app("Home", home.app)
apps.add_app("S&P", sp.app)
apps.add_app("Dow Jones", dj.app)


# The main app
apps.run()

