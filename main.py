import optimiseprime.data_prep as dp
import optimiseprime.data_analysis as da

import pandas as pd
import yfinance as yf
import quantstats as qs
qs.extend_pandas()

def main():

    portfolio_choice = ""
    while portfolio_choice not in [1, 2]:
        try:
            portfolio_choice = int(input(         
                "To analyse an existing portfolio, type 1\n"
                "To analyse a hypothetical portfolio - type 2\n"
            )
                                  )
        # Print error message if type(portfolio_choice) != int                        
        except ValueError:
            print('Error: Invalid response.\n')

        # Print error message if portfolio choice not 1 or 2
        if portfolio_choice not in [1, 2]:
            print('Error: Invalid response.\n')

    # Get portfolio data from user depending on choice:

    ticker_list = []

    while len(ticker_list) == 0:
        if portfolio_choice == 1:
            existing_portfolio = dp.get_existing_portfolio()

            # Create a list of only the tickers
            ticker_list = []
            for key, value in existing_portfolio.items():
                ticker_list.append(key)
            ticker_list = pd.DataFrame(columns=ticker_list).add_suffix('-USD').columns.tolist()

        elif portfolio_choice == 2:
            ticker_list = dp.get_hypothetical_portfolio()
            # Request investment amount from user
            portfolio_value = dp.get_investment_amt()

        if len(ticker_list) == 0:
            print("You have not entered any tickers.")
    # Keep only tickers in ticker_list for which data is available
    ticker_list = [ticker for ticker in list(portfolio_df.columns.levels[0])]

    # Print portfolio data for visual confirmation
    if portfolio_choice == 1:    
        # Calculate portfolio value of each cryptocurrency held
        for ticker in existing_portfolio:
            existing_portfolio[ticker].append(
                {'value': portfolio_df[f"{ticker}-USD"].iloc[-1, 3] * existing_portfolio[ticker][0]['units']})
        print(f"--------------------------")                      
        print(f"Existing Portfolio:")
        portfolio_value = 0
        for ticker, units in existing_portfolio.items():
            value = existing_portfolio[ticker][1]['value']
            print(f"Value of {existing_portfolio[ticker][0]['units']} {ticker}: ${value:.2f}")
            portfolio_value += value
        print(f"\nTotal portfolio value: ${portfolio_value:.2f}\n")       

    elif portfolio_choice == 2:
        print(f"--------------------------")                      
        print(f"Hypothetical Portfolio:")
        print(f"{[ticker.replace('-USD', '') for ticker in ticker_list]}")                   
        print(f"Investment amount:")
        print(f"${portfolio_value:.2f}\n")

    print(
        f"NOTE:\n"
        f"To achieve a fair comparison of risk-reward ratios, historical price data will be retrieved from earliest date for which ALL cryptocurrencies specified are available.\n"
        f"While this ensures fair comparison of risk-reward metrics, it may compromise accuracy of these metrics if the sample sizes of historical price data are reduced.\n"
        f"Earliest date for which price data is available for all cryptocurrencies in your portfolio: {dt.datetime.date(portfolio_df.index[0])}"
    )
    print(f"--------------------------")

    # Calculate each of the following risk-reward ratio types
    sharpe = da.calculate_sharpe_ratio(ticker_list, portfolio_df)
    sortino =  da.calculate_sortino_ratio(ticker_list, portfolio_df)
    adjusted_sortino = da.calculate_adjusted_sortino(ticker_list, portfolio_df)
    gain_pain_ratio = da.calculate_gain_pain_ratio(ticker_list, portfolio_df)


    # Store all ratios into a dict
    ratios_df = pd.DataFrame(
        {
        'sharpe': sharpe,
        'sortino': sortino,
        'adj_sortino': adjusted_sortino,
        'gain_pain': gain_pain_ratio,
        }
    )

    # Calculate proportion scores for each risk-reward metric
    weights = da.calculate_weights(ratios_df)

    print(
        f"Portfolio allocation recommendations\n"
        f"Based on historical returns from {dt.datetime.date(portfolio_df.index[0])} to {dt.datetime.date(portfolio_df.index[-1])}"
    )
    print(f"Total portfolio value: ${portfolio_value:.2f}")
    print(f"============================================================="
    )

    # Present all ratios in descending order

    for column in ratios_df:
        if column == 'sharpe':
            da.sharpe_portfolio(ratios_df, weights, portfolio_value)
        elif column == 'sortino':
            da.sortino_portfolio(ratios_df, weights, portfolio_value)
        elif column == 'adj_sortino':
            da.adj_sortino_portfolio(ratios_df, weights, portfolio_value)
        elif column == 'gain_pain':
            da.gain_pain_portfolio(ratios_df, weights, portfolio_value)
            
    
    # Autoregressive model forecasting
    ticker_close_names = []
    for ticker in list(weights.index):
        ticker_close_names.append((ticker, 'close'))    
        

    portfolio_close_df = portfolio_df[ticker_close_names]

    portfolio_returns_list_df = []
    for column_name in weights.columns:
        weights_list = weights[column_name].tolist()
        portfolio_returns = portfolio_close_df.dot(weights_list)
        portfolio_returns = portfolio_returns.rename(column_name)
        portfolio_returns_list_df.append(portfolio_returns)

    

if __name__ == '__main__':
    main()
    