# Optimise Prime: Optimising Crypto Portfolios

Optimise Prime is a programme that helps user analyse their current or hypothetical cryptocurrency portfolios, and provides a recommended investment weightage based on several risk metrics. 




## Keying in your crypto portfolio.

Within `fetch_data.py`, the `input_cryptos` function asks the user to key in the cryptocurrencies in their portfolio as tickers, one at a time. Each ticker will then be stored within a list. 


## Retrieval of data


Within `fetch_data.py`, the `get_crypto_data` function serves to retrieve cryptocurrency historic price data (OHLCV) using *yfinance's* `.history()` attribute.
*yfinance* is aa library that retrieves data from Yahoo! Finance's API. See library information [here](https://pypi.org/project/yfinance/).

Users are first required to select a timeframe for which the data is to be retrieved. Valid timeframes include '1d', '5d', '1wk', '1mo', and '3mo'.
Data retrieved from **yfinance** will converted into a pandas dataframe, with an extra column consisting of computed daily returns.






