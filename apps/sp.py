#Dicts with Financial statements and Quote page from Yahoo finance
from yahoo_fin import stock_info as si
from tqdm.notebook import trange, tqdm
import pickle
import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu

#with st.sidebar:
#    selected = option_menu("Main Menu", ["Home", 'Settings'], 
#        icons=['house', 'gear'], menu_icon="cast", default_index=1)
#    selected

# horizontal menu
#selected2 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'], 
#    icons=['house', 'cloud-upload', "list-task", 'gear'], 
#    menu_icon="cast", default_index=0, orientation="horizontal")
#selected2


sp_list = si.tickers_sp500()
dow_list = si.tickers_dow()
minilist = ['A','AAPL']



def app():
    st.title('Stonkotracker 5000')
    
    clicky = st.button('Fetch data')

    if clicky:
        fetch_data()
        st.write('Downloading data')

    st.header('Overall scores')
    st.subheader('Overall score')
    overall = newdf[['Ticker','Name','Overall score']].sort_values(by=['Overall score'], ascending=False)
    overall

    st.subheader('Intrinsic value')
    st.caption('Out of 2')
    intrinsic = newdf[['Ticker','Name','Intrinsic value']].sort_values(by=['Intrinsic value'], ascending=False)
    intrinsic

    st.subheader('Financial situation')
    st.caption('Out of 8')
    financial = newdf[['Ticker','Name','Financial situation']].sort_values(by=['Financial situation'], ascending=False)
    financial

    st.subheader('Earnings')
    st.caption('Out of 8')
    earnings = newdf[['Ticker','Name','Earnings']].sort_values(by=['Earnings'], ascending=False)
    earnings

    st.subheader('Dividends')
    st.caption('Out of 5')
    dividends = newdf[['Ticker','Name','Dividends']].sort_values(by=['Dividends'], ascending=False)
    dividends

    st.subheader('Relative price')
    st.caption('Out of 5')
    price = newdf[['Ticker','Name','Relative price']].sort_values(by=['Relative price'], ascending=False)
    price



    st.header('Intrinsic Value')
    st.caption('HIGHER IS BETTER. ALL METRICS = 1 WHEN THEY MEET GRAHAMS EXPECTATIONS. These metrics attempt to estimate the instrinsic value of a company, as objectively as possible, relative to the price.')

    st.subheader('Price-to-NCAV')
    st.markdown('Ignoring things like factories and equipment, how many dollars are we paying per dollar?')
    st.caption('0.66 / (Price/NCAVPS)')
    NCAVPS = newdf[['Ticker','Name','0,66/NCAVPS/Price']].sort_values(by=['0,66/NCAVPS/Price'], ascending=False)
    #NCAVPS.sort_values(by=['0,66/NCAVPS/Price'])
    NCAVPS

    st.subheader('Grahams number')
    st.markdown('Grahams number is price-to-book * price-to-earnings. You dont want to over-pay for either of them, so this metric ensures that they are both reasonable. 22.5 / Grahams Number')
    newdf[['Ticker','Name','Grahams number']].sort_values(by=['Grahams number'], ascending=False)
    grahams = newdf[['Ticker','Name','Grahams number']].sort_values(by=['Grahams number'], ascending=False)
    grahams

    st.header('Financial situation')
    st.caption('HIGHER IS BETTER. ALL METRICS = 1 WHEN THEY MEET GRAHAMS EXPECTATIONS. These metrics attempt to estimate the instrinsic value of a company, as objectively as possible, relative to the price.')

    st.subheader('Current Ratio')
    st.markdown('This is the ability to pay the liabilities in the next year with the cash and liquid assets they already have.')
    st.caption('Current Assets / [2 * Current Liabilities]')
    cr = newdf[['Ticker','Name','CurAss/2*CurLiab']].sort_values(by=['CurAss/2*CurLiab'], ascending=False)
    cr

    st.subheader('NCAV/Total Debt')
    st.caption('This is the ability to pay all debt with the cash and liquid assets they already have.')
    st.caption('(NCAV / Total Debt) / 1.1')
    nt = newdf[['Ticker','Name','NCAV/TotDebt/1.1']].sort_values(by=['NCAV/TotDebt/1.1'], ascending=False)
    nt

    st.subheader('Interest Coverage')
    st.caption('This ratio is reversed here so it gets higher when it is good. All assets - all liabiities = shareholder equity. This measures how much of the business is owned vs how much is loaned.')
    st.caption('Normalized Earnings / 7 * Interest payments on debt')
    ic = newdf[['Ticker','Name','NormEarn/7*InterestPay']].sort_values(by=['NormEarn/7*InterestPay'], ascending=False)
    ic

    st.subheader('Debt-to-Equity (reversed)')
    st.caption('This measures how well their profits cover their debt payments. "Normalized" earnings are the average of the last three years of net income.')
    st.caption('(All assets - all liabilities) / All liabilities')
    de = newdf[['Ticker','Name','AllAss-AllLiab/AllLiab']].sort_values(by=['AllAss-AllLiab/AllLiab'], ascending=False)
    de

    st.subheader('Working capital / Long term debt')
    st.caption('Long term debt = "non-current" debt.')
    st.caption('Working capital / Long Term (non-current) debt')
    wl = newdf[['Ticker','Name','Working capital / Long Term (non-current) debt']].sort_values(by=['Working capital / Long Term (non-current) debt'], ascending=False)
    wl

    st.subheader('Most recent loss')
    st.caption('NOTE: This can produce scores larger than 1 if the company has been profitable for a long time. That is intentional.')
    st.caption('[Number of years back to the most recent loss] / 5')
    mrl = newdf[['Ticker','Name','Years since most recent loss /5']].sort_values(by=['Years since most recent loss /5'], ascending=False)
    mrl

    st.subheader('Overall Size')
    st.caption('Statistically, it is much less likely for a big company to completely go out of business, therefore size is used as a proxy for safety. 500M in revenue is roughly the average for the whole stock market. Although we might want to look at smaller companies, this is a good way to stop us from overlooking the risk that comes with less revenue.')
    st.caption('Total Revenue / mean of Dow Jones')
    osd = newdf[['Ticker','Name','Total Revenue / Mean']].sort_values(by=['Total Revenue / Mean'], ascending=False)
    osd
    st.caption('Total Revenue / 500M')
    os5 = newdf[['Ticker','Name','Total Revenue / 500M']].sort_values(by=['Total Revenue / 500M'], ascending=False)
    os5

    st.header('Earnings')

    st.subheader('Stability')
    st.caption('Shouldve been 10 but only have data for the past 4 years')
    st.caption('(4 - [Number of last 4 years with an earnings decline]) / 4')
    s = newdf[['Ticker','Name','(4 - [Number of last 4 years with an earnings decline]) / 4']].sort_values(by=['(4 - [Number of last 4 years with an earnings decline]) / 4'], ascending=False)
    s

    st.subheader('Growth')
    st.caption('([Normalized earnings from the last 3 years] / [Same from 10 years earlier]) / 1.3')
    st.caption('Work In Progress')
    st.markdown("![Alt Text](https://media.giphy.com/media/DqhwoR9RHm3EA/giphy.gif)")

    st.caption('10-year CAGR / 0.07')
    st.caption('Work In Progress')
    st.markdown("![Alt Text](https://media.giphy.com/media/5Zesu5VPNGJlm/giphy.gif)")
    ecagr = habadf[['Ticker','Name','ECAGR7dec']].sort_values(by=['ECAGR7dec'], ascending=False)
    ecagr

    st.caption('"[Normalized Earnings / Normalized Revenue for last 3 years] / [1.5 * Same from 10 years earlier]"')
    st.caption('Cant do since we dont have data for revenue more than 4 years back')

    st.subheader('Profitability')


    st.caption('You seeing this shit')
    st.caption('Earnings to price yield / [2 * AAA bond rate]')
    etpy = newdf[['Ticker','Name','Earnings to price yield / [2 * AAA bond rate]']].sort_values(by=['Earnings to price yield / [2 * AAA bond rate]'], ascending=False)
    etpy

    st.caption('[Earnings / Revenue] / 0.1')
    st.caption('Work In Progress')
    st.markdown("![Alt Text](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)")


    st.caption('3-Year Normalized: Earnings-per-share / Book Value per share')
    st.caption('DONE (but shares outstanding is just for last year)')
    norm3b = habadf[['Ticker','Name','3-Year Normalized: Earnings-per-share / Book Value per share']].sort_values(by=['3-Year Normalized: Earnings-per-share / Book Value per share'], ascending=False)
    norm3b

    #norm3b = newdf[['Ticker','Name','norm3']].sort_values(by=['norm3'], ascending=False)
    #norm3b

    st.header('Dividends')

    st.caption('Some current dividend?')
    st.markdown("![Alt Text](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)")

    st.caption('Stability')
    st.caption('Total uninterrupted years with dividend / 10')
    stab = newdf[['Ticker','Name','Total uninterrupted years with dividend/10']].sort_values(by=['Total uninterrupted years with dividend/10'], ascending=False)
    stab

    st.caption('Growth')
    st.caption('[Dividend CAGR over past 20 years] + 1')
    gro = newdf[['Ticker','Name','Dividend CAGR past 20y']].sort_values(by=['Dividend CAGR past 20y'], ascending=False)
    gro

    st.caption('Profitability')
    st.caption('Dividend Yield = [payout per share / price per share] / 0.02')
    prof1 = newdf[['Ticker','Name','Dividend Yield / 0.02']].sort_values(by=['Dividend Yield / 0.02'], ascending=False)
    prof1

    st.caption('[AAA bond yield / 1.5 x Dividend Yield]')
    prof2 = newdf[['Ticker','Name','AAA bond yield / 1.5 x Dividend Yield']].sort_values(by=['AAA bond yield / 1.5 x Dividend Yield'], ascending=False)
    prof2

    st.caption('([Payout/Earnings] / Dividend Yield) / 25')
    prof3 = habadf[['Ticker','Name','([Payout/Earnings] / Dividend Yield) / 25']].sort_values(by=['([Payout/Earnings] / Dividend Yield) / 25'], ascending=False)
    prof3


    st.header('Relative price')

    st.subheader('P/E compared to market history')
    st.markdown('The historical average is about 20, so anything lower than 15 is generally "low". Low P/E values alone have been shown to correlate with better performance over the following few years.')
    st.caption('15 / (P/E)')
    pem = newdf[['Ticker','Name','15 / (P/E)']].sort_values(by=['15 / (P/E)'], ascending=False)
    pem

    st.subheader('P/E compared to company history')

    st.caption('0.4 / ((Current P/E) / Highest P/E in the last 5 years.)')
    pe1 = habadf[['Ticker','Name','currhighPE']].sort_values(by=['currhighPE'], ascending=False)
    pe1

    st.caption('[Highest P/E] / [lowest P/E] (considering the past 4 years)')
    pe2 = habadf[['Ticker','Name','[Highest P/E] / [lowest P/E] (considering the past 4 years)']].sort_values(by=['[Highest P/E] / [lowest P/E] (considering the past 4 years)'], ascending=False)
    pe2

    st.caption('(Current - 52WeekLow) / (52WeekHigh - Current)')
    pe3 = habadf[['Ticker','Name','yearlowhigh']].sort_values(by=['yearlowhigh'], ascending=False)
    pe3

    st.caption('25 / 7-year average P/E')
    st.markdown("![Alt Text](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)")
    #pe4 = newdf[['Ticker','Name','15 / (P/E)']].sort_values(by=['15 / (P/E)'], ascending=False)
    #pe4

    st.caption('20 / Trailing 12-month P/E')
    pe5 = habadf[['Ticker','Name','twentydivPE']].sort_values(by=['twentydivPE'], ascending=False)
    pe5


    st.subheader('P/E as a multiple of market average')
    st.markdown('How much we are paying for profits relative to what everyone else is paying.')
    st.caption('MA / (P/E)')
    pe6 = newdf[['Ticker','Name','MA/(P/E)']].sort_values(by=['MA/(P/E)'], ascending=False)
    pe6




