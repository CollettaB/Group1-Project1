import data_prep as dp


def main():
    
    # Initialise portfolio_choice variable
    portfolio_choice = ""
    
    # Requests user for type of portfolio to be analysed 
    while portfolio_choice not in [1, 2]:
        try:
            portfolio_choice = int(input(         
                "To analyse an existing portfolio, type 1\n"
                "To analyse a hypothetical portfolio - type 2\n"
            )
                                  )
        except Exception:
            print('Error: Invalid Choice.\n')

    # Fetch data from yfinance for each ticker, and create pandas dataframe
    portfolio_df = dp.get_ticker_data(ticker_list)
    portfolio_df.dropna(inplace = True)

    # Print portfolio data for visual confirmation
    if portfolio_choice == 1: 
        print(f"--------------------------")                      
        print(f"Cryptocurrencies selected:")
        for ticker, units in existing_portfolio.items():
            value = portfolio_df[f"{ticker}-USD"].iloc[-1, 3] * units
            print(f"{units} {ticker}")
            print(f"Value: ${value:.2f}\n")
        print(f"--------------------------")
    elif portfolio_choice == 2:
        print(f"--------------------------")                      
        print(f"Cryptocurrencies selected:")
        print(f"{[ticker.replace('-USD', '') for ticker in ticker_list]}")                   
        print(f"Investment amount:")
        print(f"${investment_amount:.2f}")
        print(f"--------------------------")
if __name__ == '__main__':
    main()
    