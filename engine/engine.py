from util.previous_date import getPreviousDay
from util.market_data import historical_data_gmd

class Hadaly_Engine:
    def __init__(self, strategy, stock_symbol: str, start_date: str, end_date: str, interval):
        self.commander = strategy
        data = historical_data_gmd(stock_symbol, getPreviousDay(start_date), end_date, interval)
        self.simulate(data, start_date, end_date)
    
    def simulate(self, data, start_date, end_date):
        self.commander.backtest_strategy(data, start_date, end_date)
        