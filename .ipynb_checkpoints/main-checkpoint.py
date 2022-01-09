import fetch_data as fd


def main():

    # Request crypto tickers from user, and record as list
    ticker_list = fd.get_portfolio_data()

    # Request investment amount from user
    investment_amount = fd.get_investment_amt()

    # Fetch data from yfinance for each ticker, and create pandas dataframe
    portfolio_df = fd.get_ticker_data(ticker_list)

    # Print portfolio data for visual confirmation
    print(f"--------------------------")                      
    print(f"Cryptocurrencies selected:")
    print(f"{[ticker.replace('-USD', '') for ticker in ticker_list]}")                   
    print(f"Investment amount:")
    print(f"${investment_amount:.2f}")
    print(f"--------------------------")  

if __name__ == '__main__':
    main()
    