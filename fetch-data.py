
import pandas as pd
import datetime
import yfinance as yf

def input_cryptos():
    '''
    Requests user to key in crypto tickers, and appends to a list
    '''
    ticker_list = []
    ticker = ""
    print("Please enter the tickers of your cryptocurrencies one by one")
    print("Type done when finished.")
    while ticker.casefold() != "done":
        ticker = str.upper(input("Ticker: "))
       
                           
        if ticker.casefold() != "done":
            ticker_list.append(ticker)
        else:
            break
                               
    print(f"Crpytocurrencies selected:")
    print(ticker_list)
    
    # Adds "-USD" suffix to each crypto ticker for compatibility with yfinance
    ticker_list = pd.DataFrame(columns=ticker_list).add_suffix('-USD').columns.tolist()
    return ticker_list

                        
# Function to get ticker data. years_back set to 3 by default, given most altcoins don't have a price history dating back more than that. 
def get_ticker_data(ticker_list, years_back = 3, freq = 'D'):
    ''''
    Fetches OHLCV data from Yahoo Finance API

    Parameters:
    ticker_list (list): A list of cryptocurrency tickers for which data is to be fetched
    years_back (int): Number of years back from the current date, for which data is to be fetched
    '''
    # Initialise dict to record OHLCV data
    d ={}
    # Define start and end dates
    end = datetime.datetime.now()
    start = datetime.datetime.now() - datetime.timedelta(days=365*2)
    # create empty dataframe
    cryptos_final = pd.DataFrame()
    
    # Get timeframe 
    interval_list = ['1d', '5d', '1wk', '1mo', '3mo']
    interval = str(input(
        f"Please select the interval: \n"
        f"(Valid intervals: 1d, 5d, 1wk, 1mo, 3mo)\n"
    )
                  )
                  
    while interval not in interval_list:
        print("\nError: You have selected an invalid interval")
        interval = str(input(
            f"Please select the interval: \n"
            f"(Valid intervals: 1d, 5d, 1wk, 1mo, 3mo)"
        )
                      )
                      
           
    for ticker in ticker_list:
        try:
            # download the crypto price 
            crypto = yf.Ticker(ticker)
            crypto_df = crypto.history(start = start, end = end, interval = interval)
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
