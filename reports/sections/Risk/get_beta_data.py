import datetime as dt
from util.market_data import get_data_yfinance as get_market_data
from talib.abstract import BETA
from typing import List, Tuple
import numpy as np

def retrieve_data(portfolio_allocation: dict) -> dict:
    """
    Retrieve enough data to calculate the beta for every stock in the portfolio

    Input:
        portfolio_allocation: Dictionnary where the keys are the stock tickers and the values are the percentage of each one in this portfolio
    
        
    """
    final_date = dt.date.today()
    debut_date = final_date - dt.timedelta(days=30)

    debut_date = debut_date.strftime('%Y-%m-%d')
    final_date = final_date.strftime('%Y-%m-%d')

    market_data_portfolio = {}
    for ticker in list(portfolio_allocation.keys()):
        market_data = get_market_data(ticker, debut_date, final_date, "1d")
        market_data_portfolio[ticker] = market_data
    return market_data_portfolio

def calculate_beta(data: List) -> np.float64:
    """
    Calculate the beta of the data provided

    Input:
        data: np.array of float values 

    Output:
        beta[-1]: the last beta value calculated (np.float64)

    """
    betas = BETA(data)
    return betas[-1]

def get_betas(portfolio_allocation: dict) -> Tuple[float, dict]:
    """
    Calculate 
    """
    OHLC_data = retrieve_data(portfolio_allocation)
    stock_betas = {}
    portfolio_beta = 0
    for stock, OHLC in OHLC_data.items():
        beta = calculate_beta(OHLC)
        stock_betas[stock] = beta
        portfolio_beta += beta * portfolio_allocation[stock]
    
    return stock_betas, portfolio_beta