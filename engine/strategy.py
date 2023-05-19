import json
from util.calculateIndicators import calculateIndicators
from engine.Stock import Stock

class Strategy:
    def __init__(self, strategyJson, cash_wallet:int = 1000, stock_wallet:int = 0):
        strategy = json.loads(strategyJson)
        
        self.cash_wallet = cash_wallet
        self.stock_wallet = stock_wallet
        
        self.strategy = self.convert_crossover(strategy)

        self.logic_entry = self.strategy['ENTRY']['LOGIC']
        self.logic_exit = self.strategy['EXIT']['LOGIC']
        self.indicators_entry = self.strategy['ENTRY']['INDICATORS']
        self.indicators_exit = self.strategy['EXIT']['INDICATORS']
        self.exposure_entry = self.strategy['ENTRY']['EXPOSURE']
        self.exposure_exit = self.strategy['EXIT']['EXPOSURE']

        self.stop_loss = 0
        self.take_profit = 0
        self.trailing_stop = 0

        if self.strategy["SECURITY"]['stop_loss']['status']==1:
            self.stop_loss = self.strategy["SECURITY"]['stop_loss']['value']

        if self.strategy["SECURITY"]['take_profit']['status']==1:
            self.take_profit = self.strategy["SECURITY"]['take_profit']['value']

        if self.strategy["SECURITY"]['trailing_stop']['status']==1:
            self.trailing_stop = self.strategy["SECURITY"]['trailing_stop']['value']

    def convert_crossover(self,strategy):
        operators=[' + ',' - ',' > ',' < ',' = ',' and ',' or ',' ( ',' ) ' , ' crossover ',' crossunder ']
        proc_strat=strategy.copy()

        if ' crossover ' in [list(h.keys())[0] for h in strategy['ENTRY']['LOGIC']]:
            proc_entry=self.convert_cross_part(proc_strat['ENTRY']['LOGIC'])
            proc_entry_indicators=[x for x in proc_entry if list(x.keys())[0] not in operators ]
            proc_strat['ENTRY']['LOGIC']=proc_entry
            proc_strat['ENTRY']['INDICATORS']=proc_entry_indicators
        if ' crossover ' in [list(h.keys())[0] for h in strategy['EXIT']['LOGIC']]:
            proc_exit=self.convert_cross_part(proc_strat['EXIT']['LOGIC'])
            proc_exit_indicators=[x for x in proc_exit if list(x.keys())[0] not in operators ]
            proc_strat['EXIT']['LOGIC']=proc_exit
            proc_strat['EXIT']['INDICATORS']=proc_exit_indicators
        return proc_strat

    def do_Strategy(self, data):
        self.data = data
        self.in_trade = 0
        self.stock_qty= self.stock_wallet / self.stock_price
        
        self.buy_move=0
        self.sell_move=0
        self.transaction_monitor=0

        dict_portfolio = {'cash_wallet': [] ,
                    'stock_wallet': [] ,
                    'port_value': [] ,
                    'stock_qty': [],
                    'stock_price': [],
                    'buy_move':[],
                    'sell_move':[],
                    'transaction_monitor': [],
                    'close_time': [],
                    'log':[],
                    'trade_return':[],
                    'move_info':[]}

        indicators_entry = calculateIndicators(data, self.indicators_entry)
        indicators_exit = calculateIndicators(data, self.indicators_exit)

        security_stock_price= data['close'][0]
        trailing_stop_price = security_stock_price * (1 - float(self.trailing_stop)/ 100)
        last_stock_price=0

        for day in range( len(data['close'])):
            stock = Stock(data)
            should_entry = self.eval_condition(self.logic_entry, self.indicators_entry, indicators_entry, day)
            should_exit = self.eval_condition(self.logic_exit, self.indicators_exit, indicators_exit, day)

            if stock.price > last_stock_price:
                trailing_stop_price = stock.price * (1-float(self.trailing_stop)/100)

            take_profit_price = security_stock_price * (1+ float(self.take_profit)/100)
            stop_loss_price = security_stock_price * (1- float(self.stop_loss))
            

    def eval_condition(self, logic, logic_indicators, indicators_value, index):
        condition =self.translate_condition(logic, logic_indicators, indicators_value, index)
        if 'nan' in condition:
            return False
        else:
            return eval(condition)
    
    def translate_condition(self, logic, logic_indicators, indicators_value, index):
        condition_list = []
        indicator_index = 0

        for i in logic:
            if i in logic_indicators:
                if list(i.values())[0].get('num'):
                    condition_list.append(list(i.values())[0].get('num'))
                else:
                    condition_list.append(indicators_value['indicators'][i][index])
                indicator_index += 1
            else:
                condition_list.append(list(i.keys())[0])
        
        condition_string = ''.join(str(e) for e in condition_list)
        return condition_string