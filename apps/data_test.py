import streamlit as st
import numpy as np
import pandas as pd
from data.data import fetch_data

def app():
    st.title('Data Stats')

    st.write("This is a sample data stats in the mutliapp.")
    st.write("See `apps/data_stats.py` to know how to use it.")

    st.markdown("### Plot Data")
    df = fetch_data()

    st.line_chart(df)
