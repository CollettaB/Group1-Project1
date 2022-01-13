from matplotlib import pyplot
from statsmodels.tsa.ar_model import AutoReg
from math import sqrt
from statsmodels.graphics.tsaplots import plot_pacf
import panel as pn
import panel.widgets as pnw
import pandas as pd

import holoviews as hv
import hvplot.pandas



def forecast_portfolio(portfolio_returns, window = 60, foward_looking = 20, full_picture =  False):
    # Visualising significant lags    
    returns_list = list(portfolio_returns.values)

    model = AutoReg(returns_list, lags = window, old_names=False)
    model_fit = model.fit()
    coef = model_fit.params

    index_list = [-num for num in sorted(list(range(1, window + 1)))]
    
    expected_list = []
    for look_foward in range(foward_looking):
        future_observation = coef[0]
        for back, coef_num in zip(index_list, coef[1:]):
            future_observation += (returns_list[back] * coef_num)
        expected_list.append(future_observation)
        returns_list.append(future_observation)
        
    if full_picture == True:
        forecasted_returns = pd.Series(returns_list).rename(portfolio_returns.name)
        return forecasted_returns
    else:
        expected_returns = pd.Series(expected_list).rename(portfolio_returns.name)
        return expected_returns

    
def forecast_all_portfolios(portfolio_returns_list, window, foward_looking, full_picture = False):
    series_list = []
    for portfolio_returns in portfolio_returns_list:
        series = forecast_portfolio(portfolio_returns, window, foward_looking, full_picture)
        series_list.append(series)
    portfolio_forecasted_returns = pd.concat(series_list, axis = 'columns', join = 'inner')
    return portfolio_forecasted_returns.hvplot()



