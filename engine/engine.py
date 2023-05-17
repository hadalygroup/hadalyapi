import json
from typing import List

class Strategy:
    def __init__(self, strategyString):
        strategy = json.loads(strategyString)
        self.setExitLogic(strategy["EXIT"]["LOGIC"])
        
    def setExitLogic(self, exitList: List[str]):
        pass

    def isEntry(self):
        pass
        

class Stock:
    def __init__(self, data):
        self.quantity = 0
        self.price = data['close'][0]
        self.close_time = data['close_time'][0]

class Portfolio:
    def __init__(self, stocks: List[Stock], wallet_value: int, stocks_value: int):
        self.stocks = stocks
        self.wallet_value = wallet_value
        self.stocks_value = stocks_value
        self.portfolio_value = wallet_value + stocks_value
        self.in_trade = 0

        for stock in self.stocks:
            self.quantity += stock.quantity
        
    def setStrategy(self, strategy)
        
        

class Hadaly_Engine:
    def __init__(self):
        self.exchange: int = 0

        self.cash_wallet: int = 0
        self.stock_wallet: int = 0

        self.port_value: int = 0
        self.stock_qty: int = 0

        self.buy_move: int = 0
        self.sell_move: int  = 0
        self.transaction_monitor: int = 0

        self.close_time = 0
        self.in_trade: int = 0

        self.portfolio: Portfolio = None
    
    

