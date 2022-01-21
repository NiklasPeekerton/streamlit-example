import streamlit as st
import numpy as np
import pandas as pd
from data.data import fetch_data

minilist = ['A', 'ACN']

def app():
    st.title('Testing data fetch/read')

    st.write("Should contain data from 2 stocks at the moment")

    st.markdown("### Plot Data")
    #df = fetch_data()

    #st.line_chart(df)
    clicky = st.button('Fetch data')

    if clicky:
        fetch_data()
        st.write('Downloading data')
    with open('Financials.pkl','rb') as read_file:
        Financialsj = pickle.load(read_file)

    with open('Quote.pkl','rb') as read_file:
        Quotej = pickle.load(read_file)

    with open('Dividends.pkl','rb') as read_file:
        Dividendsj = pickle.load(read_file)

    with open('Earnings.pkl','rb') as read_file:
        Earningsj = pickle.load(read_file)

    with open('Price.pkl','rb') as read_file:
        Pricej = pickle.load(read_file)

    keysIS = ['totalRevenue', 'netIncome', 'interestExpense']
    keysBS = ['totalLiab', 'totalCurrentAssets', 'totalCurrentLiabilities', 'longTermDebt', 'totalStockholderEquity', 'intangibleAssets', 'totalAssets']
    keysQ = ['longName', 'regularMarketPrice', 'trailingPE', 'sharesOutstanding', 'fiftyTwoWeekRange', 'epsTrailingTwelveMonths', 'bookValue', 'priceToBook', 'trailingAnnualDividendRate', 'trailingAnnualDividendYield']

    haba = []

    yearnow = pd.Timestamp.now().year
    for ticker in minilist:
        try:
            IncomeStatement = Financialsj[ticker]['yearly_income_statement']
            ist = IncomeStatement.reindex(keysIS)
            BalanceSheet = Financialsj[ticker]['yearly_balance_sheet']
            bs = BalanceSheet.reindex(keysBS)
            TR = ist.loc['totalRevenue'][0]
    TR
