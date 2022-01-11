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

haba = []

#Fetches data. Cache somehow?

def fetch_data():
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
    
    return()

clicky = st.button('Fetch data')

if clicky:
    fetch_data()
    st.write('Downloading data')

    
    
    
from datetime import datetime
import pandas as pd
from yahoo_fin import stock_info as si
import numpy as np
import pickle
sp_list = si.tickers_sp500()
dow_list = si.tickers_dow()

#@st.cache
def read_data():
#    with open('Financials.pkl','rb') as read_file:
#        Financialsj = pickle.load(read_file)
#
#    with open('Quote.pkl','rb') as read_file:
#        Quotej = pickle.load(read_file)
#
#    with open('Dividends.pkl','rb') as read_file:
#        Dividendsj = pickle.load(read_file)
#
#    with open('Earnings.pkl','rb') as read_file:
#        Earningsj = pickle.load(read_file)

    keysIS = ['totalRevenue', 'netIncome', 'interestExpense']
    keysBS = ['totalLiab', 'totalCurrentAssets', 'totalCurrentLiabilities', 'longTermDebt', 'totalStockholderEquity', 'intangibleAssets', 'totalAssets']
    keysQ = ['longName', 'regularMarketPrice', 'trailingPE', 'sharesOutstanding', 'fiftyTwoWeekRange', 'epsTrailingTwelveMonths', 'bookValue', 'priceToBook', 'trailingAnnualDividendRate', 'trailingAnnualDividendYield']

    yearnow = pd.Timestamp.now().year
    for ticker in dow_list:
        try:
            IncomeStatement = Financials[ticker]['yearly_income_statement']
            ist = IncomeStatement.reindex(keysIS)
            BalanceSheet = Financials[ticker]['yearly_balance_sheet']
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

            LN = Quote.get(ticker).get('longName')
            MP = Quote.get(ticker).get('regularMarketPrice')
            PE = Quote.get(ticker).get('trailingPE')
            SO = Quote.get(ticker).get('sharesOutstanding')
            FL = Quote.get(ticker).get('fiftyTwoWeekLow')
            FH = Quote.get(ticker).get('fiftyTwoWeekHigh')
            ETTM = Quote.get(ticker).get('epsTrailingTwelveMonths')
            BV = Quote.get(ticker).get('bookValue')
            PB = Quote.get(ticker).get('priceToBook')
            ADR = Quote.get(ticker).get('trailingAnnualDividendRate')
            ADY = Quote.get(ticker).get('trailingAnnualDividendYield')

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
            div = Dividends[ticker]
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
                #print(ticker, 'Currently no dividends')
                
            eps = []

            for ep in Earnings[ticker]:
                date = ep['startdatetime']
                ticker = ep['ticker']
                epsactual = ep['epsactual']
                #eps.append([blu['startdatetime'],blu['epsactual']])
                #eps.append([blu['epsactual']])
                #print(blu['startdatetime'][:4])
                #print(blu['epsactual'])
                eps.append([ticker,date,epsactual])

            Earndf = pd.DataFrame(eps, columns=['Ticker','Date','EPS'])
            #EPS CAGR for the past 10 years
            Earndf['Date'] = pd.to_datetime(Earndf['Date'])
            Earndf['Date'] = Earndf['Date'].dt.year
            avgeps = Earndf.groupby('Date').mean().dropna()
            avgeps10 = avgeps.iloc[-10:]
            ECAGR = ((((avgeps10.iloc[-1]/avgeps10.iloc[0])**(1/len(avgeps10.index))-1)*100))[0]
            ECAGR7 = ECAGR/0.07
            #avgeps10.iloc[-1]


            #([Normalized earnings from the last 3 years] / [Same from 10 years earlier]) / 1.3
            avgeps3norm = avgeps.iloc[-3:].mean()[0]
            avgeps10norm = avgeps.iloc[-13:-10].mean()[0]
            normeps310 = avgeps3norm / avgeps10norm /1.3
            #'Normalized 3-year per share earnings / [largest decline of the past 10 years]
            norm3decline10 = avgeps3norm / avgeps10.diff().min()[0]
            
            #3-Year Normalized: Earnings-per-share / Book Value per share
            #avgeps3norm
            BVPS = (TA3-TL3).mean()/SO
            EPS3BVPS3 = avgeps3norm/ BVPS
            #EPS3BVPS3

            #([Payout/Earnings] / Dividend Yield) / 25
            PEDY25 = ((ADR/ETTM)/ADY)/25
            #Earndf

            #[Highest P/E] / [lowest P/E] (considering the past 4 years)
            #highlowPE = PEepssum.max()/PEepssum.min()
            
            haba.append([ticker,LN, MP, PE, SO, FL, FH, ETTM, BV, PB, ADR, ADY, TR, NR, NR3, NI, NE, NE3, IE, TL, TCA, TCL, LTD, TSE, IA, TA, dayzz, NegEC, DCAGR, Divyears, norm3decline10, EPS3BVPS3, PEDY25])


        except Exception as e:
             print(ticker, e)


            

        
            

    return()

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
                                                 'Years of uninterrupted dividends',
                                                 'Normalized 3-year per share earnings / [largest decline of the past 10 years]',
                                                 '3-Year Normalized: Earnings-per-share / Book Value per share',
                                                 '([Payout/Earnings] / Dividend Yield) / 25'
                                                 
                                                ])
#0.4 / ((Current P/E) / Highest P/E in the last 5 years.), I'll 4 for now instead
#habadf['currhighPE'] = 0.4/((habadf['Trailing PE'])/(PEepssum.max()))



#Unweighted Earning Power	(1 + (10-Year Earnings CAGR + Dividend Yield) - AAA Bond Rate)


#7-Year Projected Earnings	(EPS * (Earning Power ^ 7))


#Book Value/Total Debt	(All assets - intangible assets - all liabilities - par value of senior issues) / Total Debt
habadf['BVTB'] = habadf['Book Value']/habadf['Total Liabilities']



# (52WeekHigh - Current) / (Current - 52WeekLow)
habadf['yearlowhigh'] = (habadf['Fifty Two Week High']-habadf['Market Price'])/(habadf['Market Price']-habadf['Fifty Two Week Low'])

#25 / 7-year average P/E


#20 / Trailing 12-month P/E
habadf['twentydivPE'] = 20 / habadf['Trailing PE']

read_data()

clicky2 = st.button('Read data')

if clicky2:
    read_data()
    st.write('Reading data')

NCAV = habadf['Current Assets']-habadf['Total Liabilities']
WC = habadf['Current Assets']-habadf['Current Liabilities']

newdf = pd.DataFrame(habadf['Ticker'])
newdf['Name'] = habadf['Name']
newdf['Trailing PE'] = habadf['Trailing PE']
newdf['NCAV'] = NCAV
newdf['NCAVPS'] = (NCAV)/(habadf['Shares Outstanding'])
newdf['0,66/NCAVPS/Price'] = 0.66/(habadf['Market Price']/newdf['NCAVPS'])
newdf['Book Value per share'] = habadf['Book Value']/habadf['Shares Outstanding']
newdf['CurAss/2*CurLiab'] = habadf['Current Assets']/(2*habadf['Current Liabilities'])
newdf['NCAV/TotDebt/1.1'] = (NCAV/habadf['Total Liabilities'])/1.1
newdf['NormEarn/7*InterestPay'] = habadf['Normalized earnings']/(7*-habadf['Interest expense'])
newdf['AllAss-AllLiab/AllLiab'] = (habadf['Total assets']-habadf['Total Liabilities'])/habadf['Total Liabilities']
newdf['Working capital / Long Term (non-current) debt'] = WC / habadf['Long Term Debt']
newdf['Years since most recent loss /5'] = habadf['Years since loss']/5
newdf['Total Revenue / 500M'] = habadf['TotalRevenue']/500000000
newdf['Total Revenue / Mean'] = habadf['TotalRevenue']/habadf['TotalRevenue'].mean()
newdf['MA/(P/E)'] = habadf['Trailing PE'].mean()/habadf['Trailing PE']
newdf['Grahams number'] = (22.5/(habadf['Trailing PE']*habadf['Price to Book']))
newdf['(4 - [Number of last 4 years with an earnings decline]) / 4'] = (4-habadf['Years of earnings decline'])/4
#newdf['Normalized 3-year per share earnings / [largest decline of the past 10 years]'] = DONE
#([Normalized earnings from the last 3 years] / [Same from 10 years earlier]) / 1.3, DONE
#10-year earnings CAGR / 0.07, DONE
#"[Normalized Earnings / Normalized Revenue for last 3 years] / [1.5 * Same from 10 years earlier]" CAN'T DO
newdf['Earnings to price yield / [2 * AAA bond rate]'] = (habadf['EPS TTM']/habadf['Market Price'])/(2*0.0261)
newdf['Earnings / Revenue / 0.1'] = (habadf['Net Income']/habadf['TotalRevenue'])/0.1
#3-Year Normalized: Earnings-per-share / Book Value per share, DONE (but shares outstanding is just for last year)
#newdf['Dividend?'] = habadf['Trailing Annual Dividend Rate'] >0 == True
newdf['Total uninterrupted years with dividend/10'] = habadf['Years of uninterrupted dividends']/10
newdf['Dividend CAGR past 20y'] = habadf['Dividend CAGR past 20y']
newdf['Dividend Yield / 0.02'] = habadf['Trailing Annual Dividend Yield']/0.02
newdf['AAA bond yield / 1.5 x Dividend Yield'] = 0.0261 / (1.5*habadf['Trailing Annual Dividend Yield'])
#([Payout/Earnings] / Dividend Yield) / 25, DONE
newdf['15 / (P/E)'] = 15/habadf['Trailing PE']
#0.4 / ((Current P/E) / Highest P/E in the last 5 years.)

st.title('Stonkotracker 5000')

st.title('Current Value')
newdf[['Ticker','Name','0,66/NCAVPS/Price']]
newdf[['Ticker','Name','Grahams number']]


st.title('Financial situation')
newdf[['Ticker','Name','CurAss/2*CurLiab']]
newdf[['Ticker','Name','NCAV/TotDebt/1.1']]
newdf[['Ticker','Name','NormEarn/7*InterestPay']]


    

