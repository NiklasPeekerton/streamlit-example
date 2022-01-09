#Dicts with Financial statements and Quote page from Yahoo finance
from yahoo_fin import stock_info as si
from tqdm.notebook import trange, tqdm
import pickle
import streamlit as st

sp_list = si.tickers_sp500()
dow_list = si.tickers_dow()

Financials = {}
Quote = {}
Dividends = {}
Earnings = {}

#Fetches data. Cache somehow?
@st.cache
for ticker in tqdm(dow_list):
    try:
        fin = si.get_financials(ticker)
        qut = si.get_quote_data(ticker)
        div = si.get_dividends(ticker)
        earn = si.get_earnings_history(ticker)
        Financials[ticker] = fin
        Quote[ticker] = qut
        Dividends[ticker] = div
        Earnings[ticker] = earn
    except Exception as e:
        print(ticker, e, 'contains sum bullshit')

with open('Financials.pkl', 'wb') as f:
    pickle.dump(Financials, f)

with open('Quote.pkl', 'wb') as f:
    pickle.dump(Quote, f)

with open('Dividends.pkl', 'wb') as f:
    pickle.dump(Dividends, f)

with open('Earnings.pkl', 'wb') as f:
    pickle.dump(Earnings, f)
    
    
    
    
from datetime import datetime
import pandas as pd
from yahoo_fin import stock_info as si
import numpy as np
import pickle
sp_list = si.tickers_sp500()
dow_list = si.tickers_dow()

with open('Financials.pkl','rb') as read_file:
    Financialsj = pickle.load(read_file)

with open('Quote.pkl','rb') as read_file:
    Quotej = pickle.load(read_file)
    
with open('Dividends.pkl','rb') as read_file:
    Dividendsj = pickle.load(read_file)

with open('Earnings.pkl','rb') as read_file:
    Earningsj = pickle.load(read_file)

lista = ['AAPL','AMGN']
keysIS = ['totalRevenue', 'netIncome', 'interestExpense']
keysBS = ['totalLiab', 'totalCurrentAssets', 'totalCurrentLiabilities', 'longTermDebt', 'totalStockholderEquity', 'intangibleAssets', 'totalAssets']
keysQ = ['longName', 'regularMarketPrice', 'trailingPE', 'sharesOutstanding', 'fiftyTwoWeekRange', 'epsTrailingTwelveMonths', 'bookValue', 'priceToBook', 'trailingAnnualDividendRate', 'trailingAnnualDividendYield']

yearnow = pd.Timestamp.now().year

haba = []
#TL = Financials[ticker]['yearly_income_statement'].loc['totalRevenue'][0]

for ticker in dow_list:
    try:
        IncomeStatement = Financialsj[ticker]['yearly_income_statement']
        ist = IncomeStatement.reindex(keysIS)
        BalanceSheet = Financialsj[ticker]['yearly_balance_sheet']
        bs = BalanceSheet.reindex(keysBS)
        TR = ist.loc['totalRevenue'][0]
        NR = ist.loc['totalRevenue'].mean(skipna = True)
        NR3 = ist.loc['totalRevenue'][:3].mean(skipna = True)
        NI = ist.loc['netIncome'][0]
        NE = ist.loc['netIncome'].mean(skipna = True)
        NE3 = ist.loc['netIncome'][:3].mean(skipna = True)
        IE = ist.loc['interestExpense'][0]
    
        TL = bs.loc['totalLiab'][0]
        TL3 = bs.loc['totalLiab'][:3]
        TCA = bs.loc['totalCurrentAssets'][0]
        TCL = bs.loc['totalCurrentLiabilities'][0]
        LTD = bs.loc['longTermDebt'][0]
        TSE = bs.loc['totalStockholderEquity'][0]
        IA = bs.loc['intangibleAssets'][0]
        TA = bs.loc['totalAssets'][0]
        TA3 = bs.loc['totalAssets'][:3]
    
        LN = Quotej.get(ticker).get('longName')
        MP = Quotej.get(ticker).get('regularMarketPrice')
        PE = Quotej.get(ticker).get('trailingPE')
        SO = Quotej.get(ticker).get('sharesOutstanding')
        FL = Quotej.get(ticker).get('fiftyTwoWeekLow')
        FH = Quotej.get(ticker).get('fiftyTwoWeekHigh')
        ETTM = Quotej.get(ticker).get('epsTrailingTwelveMonths')
        BV = Quotej.get(ticker).get('bookValue')
        PB = Quotej.get(ticker).get('priceToBook')
        ADR = Quotej.get(ticker).get('trailingAnnualDividendRate')
        ADY = Quotej.get(ticker).get('trailingAnnualDividendYield')
        
        #Years since last loss
        dayz = ist.loc['netIncome']
        dayztest = np.any(ist.loc['netIncome'] <0)
        if dayztest == True:
            dayzz = yearnow - dayz.index[dayz <0].year[0]
        else:
            dayzz = None
            
        #Years of earnings decline
        NegEarn = dayz.diff(periods=-1)
        NegEC = np.sum((NegEarn < 0).values.ravel())
        
        #Dividend CAGR & years of uninterrupted dividends
        div = Dividendsj[ticker]
        if div.empty:
            print(ticker, 'Has never had dividends')
            DCAGR = None
        elif div.index.year[-1] == 2021:
            a = div.groupby(div.index.year).sum()
            since2001 = a.loc[2001:]
            DCAGR = ((((since2001.iloc[-1]/since2001.iloc[0])**(1/len(since2001.index))-1)*100)+1)[0]
            
            data= a.index
            df=pd.DataFrame(data,columns=['col1'])
            df['match'] = df.col1.eq(df.col1.shift()+1).astype(int)

            #count recent number of years of uninterrupted dividends
            Divyears = 0
            divi = df['match']
            divi = list(divi)[::-1]

            for div in divi:
                if div == 1:
                    Divyears +=1
                else:
                    break
        else:
            DCAGR = None
            Divyears = None
            #print(DCAGR)
            print(ticker, 'Currently no dividends')
            
        #Uninterrupted years of dividend
        #data= a.index
        #df=pd.DataFrame(data,columns=['col1'])
        #df['match'] = df.col1.eq(df.col1.shift()+1).astype(int)

        #count recent number of years of uninterrupted dividends
        #Divyears = 0
        #divi = df['match']
        #divi = list(divi)[::-1]

        #for div in divi:
         #   if div == 1:
                #Divyears +=1
         #   else:
          #      break
        #print(ticker, count)

    except Exception as e:
        print(ticker, e)

    
    haba.append([ticker,LN, MP, PE, SO, FL, FH, ETTM, BV, PB, ADR, ADY, TR, NR, NR3, NI, NE, NE3, IE, TL, TCA, TCL, LTD, TSE, IA, TA, dayzz, NegEC, DCAGR, Divyears])
    
    habadf = pd.DataFrame(haba, columns= ['Ticker',
                                             'Name',
                                             'Market Price',
                                             'Trailing PE',
                                             'Shares Outstanding',
                                             'Fifty Two Week Low',
                                             'Fifty Two Week High',
                                             'EPS TTM',
                                             'Book Value',
                                             'Price to Book',
                                             'Trailing Annual Dividend Rate',
                                             'Trailing Annual Dividend Yield',
                                             'TotalRevenue',
                                             'Normalized revenue',
                                             'Normalized revenue 3 years',
                                             'Net Income',
                                             'Normalized earnings',
                                             'Normalized earnings 3 years',
                                             'Interest expense',
                                             'Total assets',
                                             'Total Liabilities',
                                             'Current Assets',
                                             'Current Liabilities',
                                             'Long Term Debt',
                                             'Total Stockholder Equity',
                                             'Intangible Assets',
                                             'Years since loss',
                                             'Years of earnings decline',
                                             'Dividend CAGR past 20y',
                                             'Years of uninterrupted dividends'
                                            ])

pd.set_option("display.max_rows", None, "display.max_columns", None)
habadf
