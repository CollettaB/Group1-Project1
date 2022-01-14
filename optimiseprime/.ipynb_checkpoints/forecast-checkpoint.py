from matplotlib import pyplot
from statsmodels.tsa.ar_model import AutoReg
from math import sqrt
from statsmodels.graphics.tsaplots import plot_pacf
import panel as pn
import panel.widgets as pnw
import pandas as pd
import datetime

import holoviews as hv
import hvplot.pandas


def get_dates(portfolio_returns, window, foward_looking, full_picture):
    current_date = list(portfolio_returns.index)[-1]
    forecasted_early_date = current_date + datetime.timedelta(days = 1)
    forecasted_final_date = current_date + datetime.timedelta(days = foward_looking)
    all_dates = list(portfolio_returns.index) + list(pd.date_range(start = forecasted_early_date, end = forecasted_final_date))
    if full_picture == True:
        return all_dates
    else:
        return list(pd.date_range(start = forecasted_early_date, end = forecasted_final_date))

def forecast_portfolio(portfolio_returns, window = 60, foward_looking = 20, full_picture = False):
    all_dates = get_dates(portfolio_returns, window, foward_looking, full_picture)
    
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
        forecasted_returns = pd.DataFrame({'date': all_dates, portfolio_returns.name: returns_list}).set_index('date')
        return forecasted_returns
    else:
        expected_returns = pd.DataFrame({'date':all_dates, portfolio_returns.name: expected_list}).set_index('date')
        return expected_returns

def forecast_all_portfolios(portfolio_returns_list, window, foward_looking, full_picture = False):
    series_list = []
    for portfolio_returns in portfolio_returns_list:
        series = forecast_portfolio(portfolio_returns, window, foward_looking, full_picture)
        series_list.append(series)
    portfolio_forecasted_returns = pd.concat(series_list, axis = 'columns', join = 'inner')
    return portfolio_forecasted_returns.hvplot()