import pandas as pd
import numpy as np
from yahoo_fin import stock_info as si


def fetch_data():
    for ticker in tqdm(dow_list):
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
