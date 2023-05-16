import datetime

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
    
    def buy(self, transaction_amount: int):
        if (self.cash_wallet < transaction_amount):
            raise ValueError("Insufficient funds")
        
        elif self.cash_wallet >= transaction_amount:
            self.buy_move += 1
