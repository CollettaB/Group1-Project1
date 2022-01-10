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
    return sharpe_dict

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
    return sortino_dict

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
    return adjusted_sortino_dict

def calculate_gain_pain_ratio(ticker_list, portfolio_df):
    '''
    Calculates Jack Schwager's gain-to-pain ratio, which takes the sum of all returns divided by the absolute value of the sum of all negative returns.
    Shows the ratio of net returns to the losses.   
    Returns a dict object with key value pairs of tickers and G2P ratios
    '''
    gain_to_pain_dict = {}
    for ticker in ticker_list:
        gain_to_pain_dict[ticker] = round(portfolio_df[ticker]['daily_return'].gain_to_pain_ratio(), 4)
    return gain_to_pain_dict
    

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
        ratios_prop_score[column] = ratios_df[column] / sum(ratios_df[column]) * 100
    ratios_prop_score = pd.DataFrame(ratios_prop_score)
    return ratios_prop_score