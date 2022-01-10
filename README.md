# Optimise Prime: Optimising Crypto Portfolios

Optimise Prime is a programme that helps user analyse their current or hypothetical cryptocurrency portfolios, and provides a recommended investment weightage based on several risk metrics. 

---

## Keying in your crypto portfolio.

Within `data_prep.py`
* The `get_hypothetical_portfolio` function asks the user to key in the cryptocurrencies in their portfolio as tickers, one at a time. Each ticker will then be stored within a list. 
* The `get_existing_portfolio` function asks the user to key in crypto tickers in their existing portfolio followed by the no. of units held, and records the data into a dict


## Retrieval of data


Within `data_prep.py`, the `get_ticker_data` function serves to retrieve cryptocurrency historic price data (OHLCV) using *yfinance's* `.history()` attribute.
*yfinance* is a library that retrieves data from Yahoo! Finance's API. See library information [here](https://pypi.org/project/yfinance/).

Data retrieved from **yfinance** will converted into a pandas dataframe, with an extra column consisting of computed daily returns.






