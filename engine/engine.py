import json
from typing import List
from util.previous_date import getPreviousDay
from util.market_data import historical_data_gmd
from util.calculateIndicators import calculateIndicators

class Hadaly_Engine:
    def __init__(self, input, stock_symbol: str, start_date: str, end_date: str, interval):
        #input can either be a portfolio or a strategy
        self.commander = input #commands when to sell or buy
        data = historical_data_gmd(stock_symbol, getPreviousDay(start_date), end_date, interval)
        self.simulate(self, data)
    
    def simulate(self, data):
        self.commander.do_Strategy(data)
        