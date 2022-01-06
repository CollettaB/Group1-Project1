
import pandas as pd
import datetime
import yfinance as yf

def input_portfolio():
    '''
    Request user to input tickers of cryptocurrencies they wish to fetch data for
    '''
    ticker_list = []
    ticker = ""
    print("Please enter the tickers of your cryptocurrencies one by one")
    print("Type done when finished.")
    while ticker.casefold() != "done":
        ticker = str(input("Ticker: "))
       
                           
        if ticker.casefold() != "done":
            ticker_list.append(ticker)
        else:
            break
                               
    print(f"Crpytocurrencies selected:")
    print(ticker_list)
    return ticker_list

        
ticker_list = input_portfolio()

                        

def get_ticker_data(tickers, years_back, freq = 'D'):
    '''
    Fetches OHLCV data from Yahoo Finance API

    Parameters:
    tickers (list): A list of cryptocurrency tickers for which data is to be fetched
    years_back (int): Number of years back from the current date, for which data is to be fetched
    '''
    d ={}
    # Define start and end dates
    end = datetime.datetime.now()
    start = datetime.datetime.now() - datetime.timedelta(days=365*2)
    # create empty dataframe
    cryptos_final = pd.DataFrame()

    for ticker in tickers:
        try:
            # download the crypto price 
            crypto_df = yf.Ticker(ticker).history(start = start, end = end, interval = "1d")
            crypto_df.dropna(inplace = True)
            
            # append the individual crpyto prices 
            if len(crypto_df) == 0:
                None
            else:
                d[(ticker, "open")] = crypto_df['Open']
                d[(ticker, "high")] = crypto_df['High']
                d[(ticker, "low")] = crypto_df["Low"]
                d[(ticker, "close")] = crypto_df["Close"]
                d[(ticker, "volume")] = crypto_df["Volume"]
        except Exception:
            None
    d = pd.DataFrame(d)
    return d


d = get_ticker_data(tickers, 2)
d