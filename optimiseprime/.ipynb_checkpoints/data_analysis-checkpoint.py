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
    

def calculate_weights(ratios_df):
    '''
    Converts the risk-reward ratios of each cryptocurrency to a proportion score, by dividing the ratio value against the sum of ratio values in that column. 
    If any value is <0, winsorize to 0. This would create a proportion score of 0, indicating that no weight should be allocated to the corresponding asset. 
    
    Parameters:
    ratios_df(pandas.DataFrame): A pandas dataframe containing risk-reward ratios of user specified cryptocurrencies. 
    
    '''
    weights = {}
    # Winsorize negative values to 0
    ratios_df[ratios_df < 0] = 0
    for column in ratios_df:
        weights[column] = ratios_df[column] / sum(ratios_df[column])
    weights = pd.DataFrame(weights)
    return weights

def sharpe_portfolio(ratios_df, weights, portfolio_value):
    '''
    Calculates the recommended portfolio allocations based off a set of given cryptocurrency 'proportion scores'
    Proportion scores are calculated from sharpe ratios.
    
    Parameters:
    ratios_df(pd.DataFrame): A pd.DataFrame with financial risk-reward ratios of user-specified cryptocurrencies
    weights(pd.DataFrame): A pd.DataFrame object with calculated weights for each user-specified cryptocurrency, according to the corresponding risk-reward metrics
    portfolio_value(float): The total value of the user portfolio
    '''
    print("\nMetric: Sharpe Ratio")
    print("--------------")
    sharpe_ratios = ratios_df['sharpe'].sort_values(ascending = False)
    sharpe_ratios.sort_values(ascending = False, inplace = True)
    sharpe_allocation = {}
    # Print Sharpe ratios and recommended portfolio weightings.
    for ticker, ratio in sharpe_ratios.iteritems():
        print(
            f"{ticker:<35}{ratio:.2f}",
            f"\n{'Recommended % of total portfolio':<35}{weights.loc[ticker][0]*100:.2f}%"
            )
        # Record sharpe ratios as key-value pairs in a dict
        sharpe_allocation[ticker] = portfolio_value * weights.loc[ticker][0]
        print(
            f"{'Recommended value allocation':<35}{'$'}{sharpe_allocation[ticker]:.2f}\n"
        )
              
    # Convert sharpe_allocation dict to pd.Series
    sharpe_allocation= pd.Series(sharpe_allocation)
    return sharpe_allocation


def sortino_portfolio(ratios_df, weights, portfolio_value):
    '''
    Calculates the recommended portfolio allocations based off a set of given cryptocurrency 'proportion scores'
    Proportion scores are calculated from sortino ratios.
    
    Parameters:
    ratios_df(pd.DataFrame): A pd.DataFrame with financial risk-reward ratios of user-specified cryptocurrencies
    weights(pd.DataFrame): A pd.DataFrame object with calculated weights for each user-specified cryptocurrency, according to the corresponding risk-reward metrics
    portfolio_value(float): The total value of the user portfolio
    '''
    print("\nMetric: Sortino Ratio")
    print("--------------")
    sortino_ratios = ratios_df['sortino'].sort_values(ascending = False)
    sortino_ratios.sort_values(ascending = False, inplace = True)
    sortino_allocation = {}
    # Print sortino ratios and recommended portfolio weightings.
    for ticker, ratio in sortino_ratios.iteritems():
        print(
            f"{ticker:<35}{ratio:.2f}",
            f"\n{'Recommended % of total portfolio':<35}{weights.loc[ticker][1]*100:.2f}%"
            )
        # Record sharpe ratios as key-value pairs in a dict
        sortino_allocation[ticker] = portfolio_value * weights.loc[ticker][1]
        print(
            f"{'Recommended value allocation':<35}{'$'}{sortino_allocation[ticker]:.2f}\n"
        )
    # Convert sortino_allocation dict to pd.Series
    sortino_allocation= pd.Series(sortino_allocation)
    return sortino_allocation


def adj_sortino_portfolio(ratios_df, weights, portfolio_value):
    '''
    Calculates the recommended portfolio allocations based off a set of given cryptocurrency 'proportion scores'
    Proportion scores are calculated from adj sortino ratios.
    
    Parameters:
    ratios_df(pd.DataFrame): A pd.DataFrame with financial risk-reward ratios of user-specified cryptocurrencies
    weights(pd.DataFrame): A pd.DataFrame object with calculated weights for each user-specified cryptocurrency, according to the corresponding risk-reward metrics
    portfolio_value(float): The total value of the user portfolio
    '''
    print("\nMetric: Adjusted Sortino Ratio")
    print("--------------")
    adj_sortino_ratios = ratios_df['adj_sortino'].sort_values(ascending = False)
    adj_sortino_ratios.sort_values(ascending = False, inplace = True)
    adj_sortino_allocation = {}
    # Print adj sortino ratios and recommended portfolio weightings.
    for ticker, ratio in adj_sortino_ratios.iteritems():
        print(
            f"{ticker:<35}{ratio:.2f}",
            f"\n{'Recommended % of total portfolio':<35}{weights.loc[ticker][2]*100:.2f}%"
            )
        # Record adj_sortino ratios as key-value pairs in a dict
        adj_sortino_allocation[ticker] = portfolio_value * weights.loc[ticker][2]
        print(
            f"{'Recommended value allocation':<35}{'$'}{adj_sortino_allocation[ticker]:.2f}\n"
        )
    # Convert adj_sortino_allocation dict to pd.Series
    adj_sortino_allocation= pd.Series(adj_sortino_allocation)
    return adj_sortino_allocation


def gain_pain_portfolio(ratios_df, weights, portfolio_value):
    '''
    Calculates the recommended portfolio allocations based off a set of given cryptocurrency 'proportion scores'
    Proportion scores are calculated from gain-to-pain ratios.
    
    Parameters:
    ratios_df(pd.DataFrame): A pd.DataFrame with financial risk-reward ratios of user-specified cryptocurrencies
    weights(pd.DataFrame): A pd.DataFrame object with calculated weights for each user-specified cryptocurrency, according to the corresponding risk-reward metrics
    portfolio_value(float): The total value of the user portfolio
    '''
    print("\nMetric: Gain-to-Pain Ratio")
    print("--------------")
    gain_pain_ratios = ratios_df['gain_pain'].sort_values(ascending = False)
    gain_pain_ratios.sort_values(ascending = False, inplace = True)
    gain_pain_allocation = {}
    # Print gain pain ratios and recommended portfolio weightings.
    for ticker, ratio in gain_pain_ratios.iteritems():
        print(
            f"{ticker:<35}{ratio:.2f}",
            f"\n{'Recommended % of total portfolio':<35}{weights.loc[ticker][3]*100:.2f}%"
            )
        # Record sharpe ratios as key-value pairs in a dict
        gain_pain_allocation[ticker] = portfolio_value * weights.loc[ticker][3]
        print(
            f"{'Recommended value allocation':<35}{'$'}{gain_pain_allocation[ticker]:.2f}\n"
        )
    # Convert gain_pain_allocation dict to pd.Series
    gain_pain_allocation= pd.Series(gain_pain_allocation)
    return gain_pain_allocation
