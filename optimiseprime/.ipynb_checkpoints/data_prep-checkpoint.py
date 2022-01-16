
import pandas as pd
import datetime
import yfinance as yf


def get_hypothetical_portfolio():
    '''
    Requests user to key in crypto tickers, and appends to a list.
    '''
    ticker_list = []
    ticker = ""
    print("Please enter the tickers of your cryptocurrencies one by one")
    print("Type 'done' when finished.")
    
    # Keep requesting input from user if user has not typed 'done'
    while ticker.casefold() != "done":
        ticker = str.upper(input("Ticker: "))                           
        if ticker.casefold() != "done":
            ticker_list.append(ticker)
    
    # Adds "-USD" suffix to each crypto ticker for compatibility with yfinance
    ticker_list = pd.DataFrame(columns=ticker_list).add_suffix('-USD').columns.tolist()
    return ticker_list

def get_existing_portfolio():
    '''
    Requests user to key in crypto tickers in an existing portfolio, and units of crypto held.
    Records data as a dict
    
    '''
    ticker_dict = {}
    ticker = ""
    print("Please enter the tickers of each cryptocurrency, followed by the number of units you hold:")
    print("Type 'done' when finished.")
    
    # Keep requesting input from user if user has not typed 'done'
    while ticker.casefold() != "done":
        try:
            ticker = str.upper(input("Ticker: "))
            if ticker.casefold()!= "done":
                amount = float(input("No. of units: "))
                ticker_dict[ticker + '-USD'] = []
                ticker_dict[ticker + '-USD'].append({'units': amount})
        except Exception:
            print("Invalid input. Please ensure you are keying in a valid ticker and a valid number of units.")         
    return ticker_dict

    
def get_investment_amt():
    '''
    Requests investment amount from user. 
    '''
    investment_amount = ""
    while type(investment_amount) is not float:
        try:
            investment_amount = float(input("How much do you wish to invest in total?\n"
                                            "(Please input amount without currency symbol)\n"))
        except Exception:
            print('Error: Please input a numerical value\n'
                 'Remember not to include the currency symbol\n')    
    return investment_amount
        


def get_ticker_data(ticker_list, years_back = 3):
    ''''
    Iterates through each ticker in user portfolio and fetches OHLCV data from Yahoo Finance API into a pandas dataframe. 
    Also records daily returns for each cryptocurrency as separate columns within the same dataframe.

    Parameters:
    ticker_list (list): A list of cryptocurrency tickers for which data is to be fetched
    years_back (int): Number of years back from the current date, for which data is to be fetched. Set to 3 by default
    '''
    # Initialise dict to record OHLCV data
    d ={}
    # Define start and end dates
    end = datetime.datetime.now()
    start = datetime.datetime.now() - datetime.timedelta(days= 365 * years_back)
    # create empty dataframe
    cryptos_final = pd.DataFrame()
    
                              
    for ticker in ticker_list:
        try:
            # download the crypto price 
            crypto = yf.Ticker(ticker)
            crypto_df = crypto.history(
                start = start, 
                end = end, 
                interval = '1d'
            )
            
            # append the individual crpyto prices 
            if len(crypto_df) == 0:
                None
            # Create dataframe with multiindexed columns. Data will need to be in this format for mcforecast script
            else:
                d[(ticker, "open")] = crypto_df['Open']
                d[(ticker, "high")] = crypto_df['High']
                d[(ticker, "low")] = crypto_df["Low"]
                d[(ticker, "close")] = crypto_df["Close"]
                d[(ticker, "volume")] = crypto_df["Volume"]
                d[(ticker, "daily_return")] = crypto_df['Close'].pct_change()
        except Exception:
            None
    
    d = pd.DataFrame(d)
    d = d.dropna()
    return d

def check (portfolio_choice, ticker_list, portfolio_value):
    if portfolio_choice == 1:    
        # Calculate portfolio value of each cryptocurrency held
        for ticker in existing_portfolio:
            existing_portfolio[ticker].append(
                {'value': portfolio_df[ticker].iloc[-1, 3] * existing_portfolio[ticker][0]['units']})
        print(f"--------------------------")                      
        print(f"Existing Portfolio:")
        portfolio_value = 0
        for ticker, units in existing_portfolio.items():
            value = existing_portfolio[ticker][1]['value']
            print(f"Value of {existing_portfolio[ticker][0]['units']} {ticker}: ${value:.2f}")
            portfolio_value += value
        
        for ticker, units in existing_portfolio.items():
            weight = existing_portfolio[ticker][1]['value'] / portfolio_value
            existing_portfolio[ticker][1]['weight'] = weight
            
        print(f"\nTotal portfolio value: ${portfolio_value:.2f}\n")       


        #find current weights
        print("Crypto Weights")
        print(f"The portfolio holds:")
        for ticker, units in existing_portfolio.items():
            weight_list.append(existing_portfolio[ticker][1]['weight'])
            value_list.append(existing_portfolio[ticker][1]['value'])
        pie_df = px.data.tips()
        px.pie(pie_df, values=value_list, names=ticker_list,   title="Distribution of existing portfolio", color_discrete_sequence=px.colors.sequential.RdBu).show()
    
    elif portfolio_choice == 2:
        print(
            f"--------------------------\n"
            f"Hypothetical Portfolio:\n"
            f"{[ticker.replace('-USD', '') for ticker in ticker_list]}\n"                   
            f"Investment amount:\n"
            f"${portfolio_value:.2f}\n")
    print(
        f"NOTE:\n"
        f"To achieve a fair comparison of risk-reward ratios, historical price data will be retrieved from earliest date for which ALL cryptocurrencies specified are available.\n"
        f"While this ensures fair comparison of risk-reward metrics, it may compromise accuracy of these metrics if the sample sizes of historical price data are reduced.\n"
        f"Earliest date for which price data is available for all cryptocurrencies in your portfolio: {dt.datetime.date(portfolio_df.index[0])}"
    )
    print(f"--------------------------")
    return portfolio_value
