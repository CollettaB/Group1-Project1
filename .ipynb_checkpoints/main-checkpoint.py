import fetch_data as fd


def main():
    
    # Request crypto tickers from user, and record as list
    ticker_list = fd.input_cryptos()
    
    # Fetch data from yfinance for each ticker, and create pandas dataframe
    portfolio_df = fd.get_ticker_data(ticker_list)

    
if __name__ == '__main__':
    main()
    