import streamlit as st
from multiapp import MultiApp
from apps import home, sp


PAGES = {
    "Home": home,
    "SP 500": sp
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()

st.set_page_config(layout="wide")


apps = MultiApp()

# Add all your application here

apps.add_app("Home", home.app)
apps.add_app("S&P", sp.app)
#apps.add_app("Dow Jones", dj.app)


# The main app
apps.run()
