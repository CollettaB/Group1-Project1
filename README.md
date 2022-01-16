# Optimise Prime: Optimising Crypto Portfolios

Optimise Prime is a programme that helps user analyse their current or hypothetical cryptocurrency portfolios, and provides a recommended investment weightage based on several risk metrics. 

---

## Key in your crypto portfolio.

You may select to analyse an existing portfolio or a hypothetical one.

With an existing portfolio, the programme will request the number of units you hold for that particular crypto assets, while for a hypothetical one, simply key in your crypto tickers one after another.


## Retrieval of data


The `get_ticker_data` function serves to retrieve cryptocurrency historic price data (OHLCV) using *yfinance's* `.history()` attribute.
*yfinance* is a library that retrieves data from Yahoo! Finance's API. See library information [here](https://pypi.org/project/yfinance/).

Data retrieved from **yfinance** will converted into a pandas dataframe, with an extra column consisting of computed daily returns.

---

## Risk Reward Ratio Strategies

The programme provides an analysis of the cryptoassets in the user's portfolio, as well as the overall portfolio, according to four risk-reward metrics.

**Sharpe Ratio** : Used to calculate the return earned on the portfolio given a certain amount of risk, defined here as volatility.

**Sortino Ratio** : A variation of the Sharpe ratio that takes into account "harmful" volatility (standard deviation to the downside) from overall volatility. This is thought to give a more accurate measure of whether the portfolio produces positive returns given the amount of risk invovled

**Jack Schwager's Adjusted Sortino Ratio** : The sortino ratio divided by the square root of 2, in order to give a more comparable statistic to the Sharpe ratio. See more information [here](https://jackschwager.com/market-wizards-search-part-2-the-performance-statistics-i-use/)

**Jack Schwager's Gain-To-Pain Ratio** : The sum of all returns divided by the absolute value of the sum of all negative returns. See more information [here](https://jackschwager.com/market-wizards-search-part-2-the-performance-statistics-i-use/)


### **Recommended Weightages**
The programme then computes a list of recommended portfolio weightages for each crypto asset. To do this, it takes the given ratio for the particular asset, and divides by the sum of all ratios. 

For example, if BTC has a Sharpe ratio of 1.5, and ETH has a Sharpe of 2, the recommended weightage that should be allocated to BTC would then be $1.5 \ (1.5 + 2) = 0.43 $

---

## Forecasting

Two modes of forecasting are available:
* Autoregressive modelling
* Monte Carlo Simulation

These forecasts make use of past data in order to simulate how the user's portfolio might perform in the future. These give the user an estimate of their total portfolio value given *some* amount of time, assuming efficient markets.

---

## Visualisations

Visulisations are available for the following:
* Historical performance of crypto assets and user portfolio
* Risk-reward metrics
* historical performance of portfolios recommended by each risk-reward metric
* Forecasted returns for both autoregressive modelling and Monte Carlo simulation.



