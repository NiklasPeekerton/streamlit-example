#Dicts with Financial statements and Quote page from Yahoo finance
from yahoo_fin import stock_info as si
from tqdm.notebook import trange, tqdm
import pickle
import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np



sp_list = si.tickers_sp500()
dow_list = si.tickers_dow()


Financials = {}
Quote = {}
Dividends = {}
Earnings = {}
Price = {}

#Fetches data. Cache somehow?

def fetch_data():
    for ticker in tqdm(sp_list):
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

clicky = st.button('Fetch data')

if clicky:
    fetch_data()
    st.write('Downloading data')
    

    
from datetime import datetime
import pandas as pd
from yahoo_fin import stock_info as si
import numpy as np
import pickle
#import streamlit as st
sp_list = si.tickers_sp500()
dow_list = si.tickers_dow()




#TL = Financials[ticker]['yearly_income_statement'].loc['totalRevenue'][0]

#@st.cache
#def read_data():

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
for ticker in sp_list:
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
        
        PEepssum = pricemean['close']/sumeps5['EPS']

        highlowPE = PEepssum.max()/PEepssum.min()
        
        haba.append([ticker,LN, MP, PE, SO, FL, FH, ETTM, BV, PB, ADR, ADY, 
             TR, NR, NR3, NI, NE, NE3, IE, TL, TCA, TCL, LTD, TSE, IA, 
             TA, dayzz, NegEC, DCAGR, Divyears, norm3decline10,
            EPS3BVPS3, PEDY25, highlowPE, ECAGR7dec])



    except Exception as e:
        print(ticker, e)





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
                                         '([Payout/Earnings] / Dividend Yield) / 25',
                                         '[Highest P/E] / [lowest P/E] (considering the past 4 years)',
                                         'ECAGR7dec'
                                        ])
 #0.4 / ((Current P/E) / Highest P/E in the last 5 years.), I'll 4 for now instead
habadf['currhighPE'] = 0.4/((habadf['Trailing PE'])/(PEepssum.max()))



#Unweighted Earning Power	(1 + (10-Year Earnings CAGR + Dividend Yield) - AAA Bond Rate)


#7-Year Projected Earnings	(EPS * (Earning Power ^ 7))


#Book Value/Total Debt	(All assets - intangible assets - all liabilities - par value of senior issues) / Total Debt
habadf['BVTB'] = habadf['Book Value']/habadf['Total Liabilities']



# (52WeekHigh - Current) / (Current - 52WeekLow)
habadf['yearlowhigh'] = (habadf['Fifty Two Week High']-habadf['Market Price'])/(habadf['Market Price']-habadf['Fifty Two Week Low'])

#25 / 7-year average P/E


#20 / Trailing 12-month P/E
habadf['twentydivPE'] = 20 / habadf['Trailing PE']



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
newdf['AAA bond yield / 1.5 x Dividend Yield'] =  (1.5*habadf['Trailing Annual Dividend Yield'])/0.0261
#([Payout/Earnings] / Dividend Yield) / 25, DONE
newdf['15 / (P/E)'] = 15/habadf['Trailing PE']
#0.4 / ((Current P/E) / Highest P/E in the last 5 years.)



#intrinsic value
newdf['Intrinsic value'] = newdf['0,66/NCAVPS/Price'] + newdf['Grahams number']

#Financial situation
newdf['Financial situation'] = newdf['CurAss/2*CurLiab'] + newdf['NCAV/TotDebt/1.1'] + newdf['NormEarn/7*InterestPay'] + newdf['AllAss-AllLiab/AllLiab'] + newdf['Working capital / Long Term (non-current) debt']  + newdf['Total Revenue / Mean']#+ newdf['Years since most recent loss /5']

#Earnings
newdf['Earnings'] = newdf['(4 - [Number of last 4 years with an earnings decline]) / 4'] + newdf['Earnings to price yield / [2 * AAA bond rate]'] + habadf['3-Year Normalized: Earnings-per-share / Book Value per share']

#Dividends
newdf['Dividends'] = newdf['Total uninterrupted years with dividend/10'] + newdf['Dividend CAGR past 20y'] + newdf['Dividend Yield / 0.02'] + newdf['AAA bond yield / 1.5 x Dividend Yield'] + habadf['([Payout/Earnings] / Dividend Yield) / 25']

#Relative price
newdf['Relative price'] = newdf['15 / (P/E)'] + habadf['[Highest P/E] / [lowest P/E] (considering the past 4 years)'] + habadf['yearlowhigh'] + habadf['twentydivPE'] + newdf['MA/(P/E)']# + habadf['currhighPE']

#Overall score
newdf['Overall score'] = newdf['Intrinsic value'] + newdf['Financial situation'] + newdf['Earnings'] + newdf['Dividends'] + newdf['Relative price']

st.title('Stonkotracker 5000')

st.header('Overall scores')
st.subheader('Overall score')
overall = newdf[['Ticker','Name','Overall score']].sort_values(by=['Overall score'], ascending=False)
overall

st.subheader('Intrinsic value')
intrinsic = newdf[['Ticker','Name','Intrinsic value']].sort_values(by=['Intrinsic value'], ascending=False)
intrinsic

st.subheader('Financial situation')
financial = newdf[['Ticker','Name','Financial situation']].sort_values(by=['Financial situation'], ascending=False)
financial

st.subheader('Earnings')
earnings = newdf[['Ticker','Name','Earnings']].sort_values(by=['Earnings'], ascending=False)
earnings

st.subheader('Dividends')
dividends = newdf[['Ticker','Name','Dividends']].sort_values(by=['Dividends'], ascending=False)
dividends

st.subheader('Relative price')
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




