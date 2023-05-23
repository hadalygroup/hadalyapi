import json
import numpy as np
from util.calculateIndicators import calculateIndicators
from datetime import datetime
from engine.Stock import Stock

class Strategy:
    def __init__(self, strategyJson, cash_wallet:int = 1000, stock_wallet:int = 0):
        strategy = json.loads(strategyJson)
        
        self.cash_wallet = cash_wallet
        self.stock_wallet = stock_wallet
        self.updatePortfolioValue()
        
        self.strategy = self.convert_crossover(strategy)

        self.logic_entry = self.strategy['ENTRY']['LOGIC']
        self.logic_exit = self.strategy['EXIT']['LOGIC']
        self.indicators_entry = self.strategy['ENTRY']['INDICATORS']
        self.indicators_exit = self.strategy['EXIT']['INDICATORS']
        self.exposure_entry = float(self.strategy['ENTRY']['EXPOSURE'])
        self.exposure_exit = float(self.strategy['EXIT']['EXPOSURE'])

        self.stop_loss = 0
        self.take_profit = 0
        self.trailing_stop = 0

        if self.strategy["SECURITY"]['stop_loss']['status']==1:
            self.stop_loss = float(self.strategy["SECURITY"]['stop_loss']['value'])

        if self.strategy["SECURITY"]['take_profit']['status']==1:
            self.take_profit = float(self.strategy["SECURITY"]['take_profit']['value'])

        if self.strategy["SECURITY"]['trailing_stop']['status']==1:
            self.trailing_stop = float(self.strategy["SECURITY"]['trailing_stop']['value'])

    def updatePortfolioValue(self):
        self.portfolio_value = self.cash_wallet + self.stock_wallet
        return

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

    def backtest_strategy(self, data, start_date, end_date):
        try:
            self.data = data
            self.in_trade = False
            
            self.buy_move=0
            self.sell_move=0
            self.transaction_monitor = False

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
                stock = Stock(data['close'][day], data['close_time'][day])
                should_entry = self.eval_condition(self.logic_entry, self.indicators_entry, indicators_entry, day)
                should_exit = self.eval_condition(self.logic_exit, self.indicators_exit, indicators_exit, day)

                if stock.price > last_stock_price:
                    trailing_stop_price = stock.price * (1-float(self.trailing_stop)/100)

                take_profit_price = security_stock_price * (1+ float(self.take_profit)/100)
                stop_loss_price = security_stock_price * (1- float(self.stop_loss))


                if should_entry and not self.in_trade:
                    bought, n_stocks_bought = self.buy(self.exposure_entry,stock=stock)
                    if bought:
                        security_stock_price = stock.price
                        log = 'timestamp: ' + str(stock.close_time) + '--' + str(n_stocks_bought)
                        self.in_trade = True
                        trailing_stop_price = stock.price * (1 - self.trailing_stop/100)
                        memory_buy_price = stock.price
                    else:
                        log = 'timestamp: ' + str(stock.close_time) + '------no cash available to buy------- cash available: ' + \
                            str(self.cash_wallet) + '-- trans_amount: ' + str(n_stocks_bought)
                    dict_portfolio['move_info'].append(np.nan)
                
                elif stock.price > take_profit_price and self.take_profit != 0 and self.in_trade:
                    sold, n_stocks_sold = self.sell(self.exposure_exit, stock= stock)
                    if sold:
                        security_stock_price = stock.price
                        log = 'timestamp: '+ str(stock.close_time) + '--' + 'take_profit exit at price: ' + \
                            str(take_profit_price)+ 'real exposure: ' + str(n_stocks_sold)
                        self.in_trade = False
                        trade_return = (stock.price - memory_buy_price)*100/memory_buy_price
                        dict_portfolio['trade_return'].append(trade_return)
                        dict_portfolio['move_info'].append('TP')
                    else:
                        log='timestamp: '+str(stock.close_time) + '------no stock available to sell------'
                        dict_portfolio['move_info'].append(np.nan)

                elif should_exit and self.in_trade:
                    sold, n_stocks_sold = self.sell(self.exposure_exit, stock=stock)
                    if sold:
                        security_stock_price = stock.price
                        log='timestamp: '+str(stock.close_time)+'--',"sell_exposure: "+str(n_stocks_sold)
                        self.in_trade = False
                        trade_return = (stock.price-memory_buy_price)*100/memory_buy_price
                        dict_portfolio['trade_return'].append(trade_return)
                        dict_portfolio['move_info'].append('exit')
                    else:
                        log='timestamp: '+ str(stock.close_time)+'--'+'------no stock available to sell------'
                        dict_portfolio['move_info'].append(np.nan)

                elif stock.price < stop_loss_price and self.stop_loss != 0 and self.in_trade:
                    sold, n_stocks_sold = self.sell(self.exposure_exit, stock=stock)
                    if sold:
                        security_stock_price = stock.price
                        log='timestamp: '+str(stock.close_time)+'--'+'stop_loss exit at price: '+ str(stop_loss_price)
                        self.in_trade=0
                        trade_return=(stock.price - memory_buy_price) * 100 / memory_buy_price
                        dict_portfolio['trade_return'].append(trade_return)
                        dict_portfolio['move_info'].append('SL')
                    else:
                        log='timestamp: '+str(stock.close_time)+'--'+'------no stock available to sell------'
                        dict_portfolio['move_info'].append(np.nan)

                elif stock.price < trailing_stop_price and self.trailing_stop != 0 and self.in_trade:
                    sold, n_stocks_sold=self.sell(self.exposure_exit)
                    if sold:
                        security_stock_price=self.stock_price
                        log='timestamp: '+ str(stock.close_time)+'--'+'trailing_stop exit at price: '+str(trailing_stop_price)
                        self.in_trade = False
                        trade_return=(stock.price - memory_buy_price) * 100 / memory_buy_price
                        dict_portfolio['trade_return'].append(trade_return)
                        dict_portfolio['move_info'].append('TS')
                    else:
                        log='timestamp: '+ str(stock.close_time)+'--'+'------no stock available to sell------'
                        dict_portfolio['move_info'].append(np.nan)
                    
                else:
                    self.buy_move = 0
                    self.sell_move = 0
                    self.transaction_monitor = False
                    self.updatePortfolioValue()
                    log='timestamp: '+ str(stock.close_time)+'--'+'no transaction: business decision'
                    dict_portfolio['move_info'].append(np.nan)
                last_stock_price = stock.price  
                dict_portfolio = self.update_portfolio_info(dict_portfolio)
                dict_portfolio = self.addPerformance(dict_portfolio,start_date, end_date)

        except Exception as e:
            print('error in backtest_strategy: ', e)
        return dict_portfolio

    def addPerformance(self, portfolio, start_date, end_date):
        start_date_index = self.find_date_index(start_date, portfolio=portfolio)
        end_date_index = self.find_date_index(end_date, portfolio=portfolio)
        stock_prices = portfolio['stock_price']
        portfolio_values = portfolio['port_value']
        market_performance = (stock_prices[end_date_index] - stock_prices[start_date_index]) * 100 / stock_prices[start_date_index]
        strat_performance = (portfolio_values[end_date_index] - portfolio_values[start_date_index]) * 100 / portfolio_values[start_date_index]
        portfolio['market_perf'] = market_performance
        portfolio['strat_perf'] = strat_performance
        portfolio['start_date_index'] = start_date_index
        portfolio['end_date_index'] = end_date_index
        if len(portfolio['trade_return']) > 0:
            portfolio['average_trade_ratio'] = sum(portfolio['trade_return'])/(len(portfolio['trade_return']))                                            
        else:
            portfolio['average_trade_ratio'] = 0
        return portfolio

    def find_date_index(self, date, portfolio):
        date = datetime.strftime(date, "%Y-%m-%d")
        date_index = portfolio['close_time'].index(date)
        return date_index
    
    def update_portfolio_info(self,dict_portfolio):
        dict_portfolio['cash_wallet'].append(self.cash_wallet)
        dict_portfolio['stock_wallet'].append(self.stock_wallet)
        dict_portfolio['port_value'].append(self.port_value)
        dict_portfolio['stock_qty'].append(self.stock_qty)
        dict_portfolio['stock_price'].append(self.stock_price)
        dict_portfolio['buy_move'].append(self.buy_move)
        dict_portfolio['sell_move'].append(self.sell_move)
        dict_portfolio['transaction_monitor'].append(self.transaction_monitor)
        dict_portfolio['close_time'].append(self.close_time)
        return dict_portfolio
    
    def buy(self, transaction_amount: float, stock: Stock):
        trade_qty = int(transaction_amount/stock.price)
        transaction_amount = trade_qty * stock.price #Met le vrai prix (on ne peut pas acheter des quarts d'actions)
        if self.cash_wallet >= transaction_amount:
            buy_result = self.validateBuy(transaction_amount= transaction_amount, trade_qty= trade_qty)
        elif self.cash_wallet < transaction_amount and self.cash_wallet > 1:
            buy_result = self.validateBuy(transaction_amount= transaction_amount, trade_qty= trade_qty)
        else:
            self.buy_move = 0
            self.transaction_monitor = False
            self.updatePortfolioValue()
            trade_qty = 0
            buy_result = False
        return buy_result, trade_qty
    
    def validateBuy(self, transaction_amount: float, trade_qty: int):
        self.sell_move = 0
        self.buy_move = 1
        self.cash_wallet -= transaction_amount
        self.stock_wallet += transaction_amount
        self.updatePortfolioValue()
        self.stock_qty += trade_qty
        self.transaction_monitor = True
        return True
    
    def sell(self, transaction_amount: float, stock: Stock):
        trade_qty = int(transaction_amount/stock.price)
        transaction_amount = trade_qty * stock.price
        if self.stock_wallet >= transaction_amount:
            sell_result = self.validateSell(transaction_amount,trade_qty = trade_qty)

        elif self.stock_wallet < transaction_amount and self.stock_wallet > 1:
            sell_result = self.validateSell(transaction_amount, trade_qty = trade_qty)
        
        else:
            self.sell_move = 0
            self.transaction_monitor = False
            self.updatePortfolioValue()
            sell_result = False
            trade_qty = 0
        return sell_result, trade_qty


    def validateSell(self, transaction_amount: float, trade_qty: int):
        self.buy_move = 0
        self.sell_move = 1
        self.cash_wallet += transaction_amount
        self.stock_wallet -= transaction_amount
        self.updatePortfolioValue()
        self.stock_qty -= trade_qty
        self.transaction_monitor = True
        return True

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