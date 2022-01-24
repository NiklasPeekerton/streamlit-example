import streamlit as st
import numpy as np
import pandas as pd
from data.data import fetch_data
import pickle
import pathlib

minilist = ['A', 'ACN']



def app():
    Financials = {}
    Quote = {}
    Dividends = {}
    Earnings = {}
    Price = {}

    #Fetches data. Cache somehow?

    def fetch_data():
        for ticker in tqdm(minilist):
            try:
                fin = si.get_financials(ticker, yearly=True, quarterly=False)
                qut = si.get_quote_data(ticker)
                div = si.get_dividends(ticker)
                earn = si.get_earnings_history(ticker)
                price = si.get_data(ticker,interval='1mo')
                Financials[ticker] = fin
                Quote[ticker] = qut
                Dividends[ticker] = div
                Earnings[ticker] = earn
                Price[ticker] = price
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

        with open('Price.pkl', 'wb') as f:
            pickle.dump(Price, f)

        return()
    st.title('Testing data fetch/read')

    st.write("Should contain data from 2 stocks at the moment")

    #st.markdown("### Plot Data")
    #df = fetch_data()

    #st.line_chart(df)
    clicks = st.button('Fetch data', key='1')

    if clicks:
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
    print(Financialsj)

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
            #PE = Quotej.get(ticker).get('trailingPE')
            SO = Quotej.get(ticker).get('sharesOutstanding')
            FL = Quotej.get(ticker).get('fiftyTwoWeekLow')
            FH = Quotej.get(ticker).get('fiftyTwoWeekHigh')
            ETTM = Quotej.get(ticker).get('epsTrailingTwelveMonths')
            BV = Quotej.get(ticker).get('bookValue')
            PB = Quotej.get(ticker).get('priceToBook')
            ADR = Quotej.get(ticker).get('trailingAnnualDividendRate')
            ADY = Quotej.get(ticker).get('trailingAnnualDividendYield')



            #Years of earnings decline
            inc = ist.loc['netIncome']
            NegEarn = inc.diff(periods=-1)
            NegEC = np.sum((NegEarn < 0).values.ravel())

            #Dividend CAGR & years of uninterrupted dividends
            div = Dividendsj[ticker]
            if div.empty:
                print(ticker, 'Has never had dividends')
                DCAGR = None
            elif div.index.year[-1] == 2021:
                a = div.groupby(div.index.year).sum()
                since2001 = a.loc[2001:]
                DCAGR = ((((since2001.iloc[-1]/since2001.iloc[0])**(1/len(since2001.index))-1))+1)[0]

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

            for ep in Earningsj[ticker]:
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
            Earndf2 = Earndf.dropna()
            avgeps = Earndf2.groupby('Date').mean()
            sumeps = Earndf2.groupby('Date').sum()
            sumeps5 = sumeps.iloc[-6:-1]
            sumeps10 = sumeps.iloc[-11:-1]
            avgeps10 = avgeps.iloc[-10:]
            ECAGRproc = ((((sumeps10.iloc[-1]/sumeps10.iloc[0])**(1/len(sumeps10.index))-1)*100))[0]
            ECAGRdec = ((((sumeps10.iloc[-1]/sumeps10.iloc[0])**(1/len(sumeps10.index))-1)))[0]
            ECAGR7dec = ECAGRdec/0.07
            #avgeps10.iloc[-1]

            #Years since last loss
            dayz = Earndf['EPS']
            dayztest = np.any(Earndf['EPS'] <0)
            dayz2 = Earndf.set_index('Date')
            if dayztest == True:
                dayzz = yearnow - dayz2.index[dayz <0][0]
            else:
                dayzz = None


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
            price = Pricej[ticker]
            price.index = price.index.year
            pricemean = price.groupby(price.index).mean()

            #Our own PE, calculated from the sum of the previous 4 quarters EPS and dividing the price with that number. Differs from Yahoo finance own calculation
            PE2 = MP/sumeps[-1:].iloc[0]

            PEepssum = pricemean['close']/sumeps5['EPS']

            highlowPE = PEepssum.max()/PEepssum.min()
            
            PEmax = PEepssum.max()

            haba.append([ticker,LN, MP, #PE,
                         SO, FL, FH, ETTM, BV, PB, ADR, ADY, 
                 TR, NR, NR3, NI, NE, NE3, IE, TL, TCA, TCL, LTD, TSE, IA, 
                 TA, dayzz, NegEC, DCAGR, Divyears, norm3decline10,
                EPS3BVPS3, PEDY25, highlowPE, ECAGR7dec, PE2[0], PEmax])



        except Exception as e:
            print(ticker, e)

        except ValueError as ve:
            print(ticker, ve)





    habadf = pd.DataFrame(haba, columns= ['Ticker',
                                             'Name',
                                             'Market Price',
                                             #'Trailing PE',
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
                                             '([Payout/Earnings] / Dividend Yield) / 25',
                                             '[Highest P/E] / [lowest P/E] (considering the past 4 years)',
                                             'ECAGR7dec',
                                             'PE calculated from EPS',
                                             'Max PE'
                                            ])
     #0.4 / ((Current P/E) / Highest P/E in the last 5 years.), I'll 4 for now instead
    habadf['currhighPE'] = 0.4/((habadf['PE calculated from EPS'])/habadf['Max PE'])
    st.dataframe(habadf)
    
    st.write("Does it get this far")
