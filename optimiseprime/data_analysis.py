import pandas as pd
import quantstats as qs
qs.extend_pandas()

def calculate_sharpe_ratio(ticker_list, portfolio_df):
    '''
    Calculates the sharpe ratios of each cryptocurrency specified in ticker_list from the daily returns column in portfolio_df.
    Returns a dict object with key value pairs of tickers and sharpe ratios
    
    Parameters:
    ticker_list(list): List of crypto tickers in user portfolio
    portfolio_df(DataFrame): Pandas dataframe containing OHLCV + daily returns data for each cryptocurrency in user portfolio
    '''
    sharpe_dict = {}
    for ticker in ticker_list:
        sharpe_dict[ticker] = round(portfolio_df[ticker]['daily_return'].sharpe(periods = 365), 4)
    sharpe_series = pd.Series(sharpe_dict)
    return sharpe_series

def calculate_sortino_ratio(ticker_list, portfolio_df):
    '''
    Calculates the sortino ratios of each cryptocurrency specified in ticker_list from the daily returns column in portfolio_df.
    Returns a dict object with key value pairs of tickers and sortino ratios
    
    Parameters:
    ticker_list(list): List of crypto tickers in user portfolio
    portfolio_df(DataFrame): Pandas dataframe containing OHLCV + daily returns data for each cryptocurrency in user portfolio
    '''
    sortino_dict = {}
    for ticker in ticker_list:
        sortino_dict[ticker] = round(portfolio_df[ticker]['daily_return'].sortino(periods = 365), 4)
    sortino_series = pd.Series(sortino_dict)
    return sortino_series

def calculate_adjusted_sortino(ticker_list, portfolio_df):
    '''
    Calculates the Jack Schwager's version of the Sortino ratio, which allows for direct comparisons to Sharpe ratio.
    More info @ https://archive.is/2rwFW#selection-583.134-583.238
    Returns a dict object with key value pairs of tickers and adjusted sortino ratios
    
    Parameters:
    ticker_list(list): List of crypto tickers in user portfolio
    portfolio_df(DataFrame): Pandas dataframe containing OHLCV + daily returns data for each cryptocurrency in user portfolio
    '''
    adjusted_sortino_dict = {}
    for ticker in ticker_list:
        adjusted_sortino_dict[ticker] = round(portfolio_df[ticker]['daily_return'].adjusted_sortino(periods  = 365), 4)
    adjusted_sortino_series = pd.Series(adjusted_sortino_dict)
    return adjusted_sortino_series

def calculate_gain_pain_ratio(ticker_list, portfolio_df):
    '''
    Calculates Jack Schwager's gain-to-pain ratio, which takes the sum of all returns divided by the absolute value of the sum of all negative returns.
    Shows the ratio of net returns to the losses.   
    Returns a dict object with key value pairs of tickers and G2P ratios
    '''
    g2p_dict = {}
    for ticker in ticker_list:
        g2p_dict[ticker] = round(portfolio_df[ticker]['daily_return'].gain_to_pain_ratio(), 4)
    g2p_series = pd.Series(g2p_dict)
    return g2p_series
    

def calculate_proportion_score(ratios_df):
    '''
    Converts the risk-reward ratios of each cryptocurrency to a proportion score, by dividing the ratio value against the sum of ratio values in that column. 
    If any value is <0, winsorize to 0. This would create a proportion score of 0, indicating that no weight should be allocated to the corresponding asset. 
    
    Parameters:
    ratios_df(pandas.DataFrame): A pandas dataframe containing risk-reward ratios of user specified cryptocurrencies. 
    
    '''
    ratios_prop_score = {}
    # Winsorize negative values to 0
    ratios_df[ratios_df < 0] = 0
    for column in ratios_df:
        ratios_prop_score[column] = ratios_df[column] / sum(ratios_df[column])
    ratios_prop_score = pd.DataFrame(ratios_prop_score)
    return ratios_prop_score

def sharpe_portfolio(sharpe_ratios, ratio_prop_score, portfolio_value):
    '''
    Calculates the recommended portfolio allocations based off a set of given cryptocurrency 'proportion scores'
    Proportion scores are calculated from sharpe ratios.
    
    Parameters:
    sharpe_ratios(pd.Series): A Series object with sharpe ratios of user-specified cryptocurrencies
    ratio_prop_score(pd.DataFrame): A pd.DataFrame object with proportion scores for each user-specified cryptocurrency, calculated from the corresponding risk-reward metrics
    portfolio_value(float): The total value of the user portfolio
    '''
    print("\nMetric: Sharpe Ratio")
    print("--------------")
    sharpe_ratios.sort_values(ascending = False, inplace = True)
    sharpe_recommended_amt = {}
    # Print Sharpe ratios and recommended portfolio weightings.
    for ticker, ratio in sharpe_ratios.iteritems():
        print(f"{ticker}: {ratio:.2f}")
        print(f"Recommended percentage of total portfolio: {ratio_prop_score.loc[ticker][0]*100:.2f}%")
        
        # Record sharpe ratios as key-value pairs in a dict
        sharpe_recommended_amt[ticker] = portfolio_value * ratio_prop_score.loc[ticker][0]
        print(f"Recommended value allocation = ${sharpe_recommended_amt[ticker]:.2f}\n")
    # Convert sharpe_recommended_amt dict to pd.Series
    sharpe_recommended_amt = pd.Series(sharpe_recommended_amt)
