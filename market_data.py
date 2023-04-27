import yahoo_fin.stock_info as si
import pandas as pd
import datetime as dt
#from binance.binance_config import config
import numpy as np
import yfinance as yf
from binance.client import Client
from datetime import datetime, date, timedelta
import time
import traceback
import ccxt
import cryptocompare


"""
Function name: historical_data
Description: Retrieves historical data of a stock using different data providers
(e.g. Binance, Yahoo Finance, yfinance) and returns a dictionary of the data.
Inputs:
STOCK_ID: string, the stock ID/symbol
START_DATE: string, the start date of the data in the format 'YYYY-MM-DD'
END_DATE: string, the end date of the data in the format 'YYYY-MM-DD'
TIME_INTERVAL: string, the time interval of the data (e.g. '1d' for daily data)
PRE_PERIOD: int, optional, the number of days before the start date to retrieve data
Outputs:
A dictionary containing the following keys: 'open', 'high', 'low', 'close',
'volume', 'close_time' with values as numpy arrays.
Called functions:
get_data_binance(STOCK_ID,START_DATE,END_DATE,TIME_INTERVAL)
get_data_yfin(STOCK_ID,START_DATE,END_DATE,TIME_INTERVAL)
get_data_yfinance(STOCK_ID,START_DATE,END_DATE,TIME_INTERVAL)
"""



def historical_data_gmd(STOCK_ID,
                        START_DATE,
                        END_DATE,
                        TIME_INTERVAL,  PRE_PERIOD=0):
    print('\n --- ',STOCK_ID,' ---\n')
    # import pandas as pd
    # import datetime as dt
    # #from binance.binance_config import config
    # import numpy as np
    # import yfinance as yf
    # from datetime import datetime
    # import numpy as np
    START_DATE=(datetime.strptime(START_DATE,'%Y-%m-%d') - timedelta(days=PRE_PERIOD)).strftime('%Y-%m-%d')
    #print('new_start_date: ',START_DATE)
    inputs = 0

    if '/' in STOCK_ID:
        inputs=get_data_cryptocompare(STOCK_ID=STOCK_ID,
                        START_DATE=START_DATE,
                        END_DATE=END_DATE,
                        TIME_INTERVAL=TIME_INTERVAL)

    if inputs==0 and '/' in STOCK_ID:
        inputs=get_data_binance(STOCK_ID=STOCK_ID,
                        START_DATE=START_DATE,
                        END_DATE=END_DATE,
                        TIME_INTERVAL=TIME_INTERVAL)

    if inputs==0 and '/' in STOCK_ID:
        inputs=get_data_kucoin(STOCK_ID=STOCK_ID,
                        START_DATE=START_DATE,
                        END_DATE=END_DATE,
                        TIME_INTERVAL=TIME_INTERVAL)

    if inputs==0:
        inputs=get_data_yfin(STOCK_ID=STOCK_ID,
                        START_DATE=START_DATE,
                        END_DATE=END_DATE,
                        TIME_INTERVAL=TIME_INTERVAL)
    if inputs==0:
        inputs=get_data_yfinance(STOCK_ID=STOCK_ID,
                        START_DATE=START_DATE,
                        END_DATE=END_DATE,
                        TIME_INTERVAL=TIME_INTERVAL)
    if inputs==0:
        inputs=  {
            'open': np.array([1,1,1,1]),
            'high': np.array([5,5,5,5]),
            'low': np.array([0,0,0,0]),
            'close': np.array([3,3,3,3]),
            'volume': np.array([7,7,7,7]),
            'close_time': np.array(['2021-01-04T00:00:00.000000000', '2021-01-05T00:00:00.000000000',
        '2021-01-06T00:00:00.000000000', '2021-01-07T00:00:00.000000000'])}
        print('---data not retrieve---')
    return inputs

"""
Function name: get_data_binance
Description: The function uses the Binance API to retrieve historical klines
(candlestick) data for a specific stock and time interval. The function takes four inputs:
STOCK_ID (the stock symbol), START_DATE, END_DATE, and TIME_INTERVAL. The function returns
a dictionary containing the 'open', 'high', 'low', 'close', 'volume' and 'close_time' for
the given stock and interval.
Inputs:
STOCK_ID (str): the stock symbol
START_DATE (str): the start date in format 'YYYY-MM-DD'
END_DATE (str): the end date in format 'YYYY-MM-DD'
TIME_INTERVAL (str): the interval of time for which to retrieve data, such as '1m' for
1 minute, '1h' for 1 hour, etc.
Outputs:
inputs (dict): a dictionary containing the 'open', 'high', 'low', 'close', 'volume'
and 'close_time' for the given stock and interval.
Called functions:
Client()
client.get_historical_klines(symbol,interval, start_str, end_str)
pd.DataFrame
data.columns
data.astype
data['open'].to_numpy()
data['high'].to_numpy()
data['low'].to_numpy()
data['close'].to_numpy()
data['volume'].to_numpy()
data['close_time'].to_numpy()
Note: This function uses the python-binance library and requires an API key and secret
to work. The actual API call has been commented out in the code.
"""

def get_data_binance(STOCK_ID,START_DATE,END_DATE,TIME_INTERVAL):
    try:
        #client = Client('api_key', 'api_secret')
        #pairs = pd.DataFrame.from_dict(client.get_all_tickers())['symbol'].to_list()
        #crypto_list_sorted = pd.DataFrame.from_dict(client.get_all_tickers()).sort_values(by=['symbol'], ascending=True)['symbol'].to_list()
        # from binance.client import Client
        # from datetime import datetime, date, timedelta
        # import datetime as dt
        # import pandas as pd
        client=Client()
        klines = client.get_historical_klines(symbol=STOCK_ID.upper(),interval= TIME_INTERVAL , start_str=START_DATE, end_str=END_DATE)
        data = pd.DataFrame(klines)
         # create colums name
        data.columns = ['open_time','open', 'high', 'low', 'close', 'volume','close_time', 'qav','num_trades','taker_base_vol','taker_quote_vol', 'ignore']
        data=data.astype(float)
        inputs = {
            'open': data['open'].to_numpy(),
            'high': data['high'].to_numpy(),
            'low': data['low'].to_numpy(),
            'close': data['close'].to_numpy(),
            'volume': data['volume'].to_numpy(),
            'close_time': data['close_time'].to_numpy()}
        print('data retrieved')
    except Exception as e:
        #print(e)
        print('did not managed to get data from binance')
        inputs=0
    return inputs



        ######################## KUCOIN ############################
"""
Function name: get_data_kucoin
Description: Retrieves historical data of an asset on the Kucoin exchange in the given time period and returns a dictionary of the data.
Inputs:
STOCK_ID: string, the stock ID/symbol
START_DATE: string, the start date of the data in the format 'YYYY-MM-DD'
END_DATE: string, the end date of the data in the format 'YYYY-MM-DD'
TIME_INTERVAL: string, the time interval of the data (e.g. '1d' for daily data)
Outputs:
A dictionary containing the following keys: 'open', 'high', 'low', 'close','volume','close_time' with values as numpy arrays.
If the function fails to retrieve the data from kucoin, it returns 0.
Called functions:
ccxt.kucoin()
exchange.load_markets()
exchange.fetch_ohlcv()
pd.DataFrame()
"""

def get_data_kucoin(STOCK_ID,START_DATE,END_DATE,TIME_INTERVAL):
    try:
        exchange_id = 'kucoin'
        exchange_class = getattr(ccxt, exchange_id)
        exchange = exchange_class({
                'apiKey':"",
                'secret': ""})

        trading_symbol = STOCK_ID #on garde BTC/USDT POUR L'INSTANT, A ADAPTER...

        #convertir en ms (https://docs.ccxt.com/en/latest/manual.html#date-based-pagination)
        start_date = START_DATE + 'T00:00:00Z'
        since = exchange.parse8601(start_date)

        #END_DATE = "2022-01-08"
        end_date = END_DATE + 'T00:00:00Z'
        end_date_ms = exchange.parse8601(end_date)
        limit = int((end_date_ms - since)/86400000)

        #donnee
        data = exchange.fetch_ohlcv(trading_symbol, timeframe=TIME_INTERVAL, since=since, limit=limit,)
        data=pd.DataFrame(data,columns=['close_time', 'open','high','low','close','volume'])
        data=data.astype(float)
        inputs = {
            'open': data['open'].to_numpy(),
            'high': data['high'].to_numpy(),
            'low': data['low'].to_numpy(),
            'close': data['close'].to_numpy(),
            'volume': data['volume'].to_numpy(),
            'close_time': data['close_time'].to_numpy()}
        print('data retrieved from kucoin')
    except Exception as e:
        print('did not managed to get data from kucoin, error: ',e)
        inputs=0
    return inputs

## CRYPTOCOMPARE ##
def get_data_cryptocompare(STOCK_ID,START_DATE,END_DATE,TIME_INTERVAL):
    try:
        crypto, currency = STOCK_ID.split("/")

        start_date = datetime.strptime(START_DATE, '%Y-%m-%d') #str to date format
        start_date_ms = start_date.timestamp()*1000 #date to ms

        end_date_nf = datetime.strptime(END_DATE , '%Y-%m-%d')
        end_date_ms = end_date_nf.timestamp()*1000

        year = int(end_date_nf.strftime('%Y'))
        month = int(end_date_nf.strftime('%m'))
        day = int(end_date_nf.strftime('%d'))

        if TIME_INTERVAL == '1d':
            limit = int((end_date_ms - start_date_ms)/86400000) #limit en JOUR
            data = cryptocompare.get_historical_price_day(crypto, currency, limit=limit, exchange='binance', toTs=datetime(year,month,day))

        if TIME_INTERVAL == '1h':
            limit = int((end_date_ms - start_date_ms)/3600000) #limit en HEURES
            data = cryptocompare.get_historical_price_hour(crypto, currency, limit=limit, exchange='binance', toTs=datetime(year,month,day))

        data=pd.DataFrame(data,columns=['time', 'open','high','low','close','volumefrom'])

        data['time']=data['time']*1000 #time converti en ms

        inputs = {  'open': data['open'].to_numpy(),
            'high': data['high'].to_numpy(),
            'low': data['low'].to_numpy(),
            'close': data['close'].to_numpy(),
            'volume': data['volumefrom'].to_numpy(),
            'close_time': data['time'].to_numpy()}
        print('data retrieved from cryptocompare')
    except Exception as e:
        print('did not managed to get data from cryptocompare')
        inputs=0
    return inputs


"""
Function name: get_data_yfin
Description: This function retrieves historical stock data for a given stock symbol,
start date, end date, and time interval from the yahoo_fin library.
Inputs:
STOCK_ID (string): the stock symbol of the stock whose data is being retrieved
START_DATE (string): the start date of the data range in the format 'yyyy-mm-dd'
END_DATE (string): the end date of the data range in the format 'yyyy-mm-dd'
TIME_INTERVAL (string): the time interval of the data (e.g. '1d' for daily data, '1m' for monthly data)
Outputs:
inputs (dictionary): a dictionary containing the stock data. The keys of the dictionary
are 'open', 'high', 'low', 'close', 'volume', 'close_time' and the values are numpy arrays.
Called functions:
si.get_data() from the yahoo_fin library
datetime.strptime() from the datetime library
datetime.strftime() from the datetime library
datetime.timestamp() from the datetime library
"""

def get_data_yfin(STOCK_ID,START_DATE,END_DATE,TIME_INTERVAL):
    # from datetime import datetime
    try:
        # from datetime import datetime, date, timedelta
        # import datetime as dt
        start_date_nf=datetime.strptime(START_DATE , '%Y-%m-%d')
        end_date_nf=datetime.strptime(END_DATE , '%Y-%m-%d')
        start_date_nf=datetime.strftime(start_date_nf,"%m/%d/%Y" )
        end_date_nf=datetime.strftime(end_date_nf,"%m/%d/%Y" )
        # print(start_date>end_date)
        # #.strftime("%d/%m/%Y" )
        # print(start_date_nf>end_date_nf)
        # import pandas as pd
        # import yahoo_fin.stock_info as si
        data=si.get_data(STOCK_ID,
                         start_date = start_date_nf,
                         end_date = end_date_nf,
                         interval=TIME_INTERVAL)
        data['close_time']=data.index
        # data['close_time']=pd.to_datetime(data['close_time']).astype('float')

        inputs = {  'open': data['open'].to_numpy(),
                        'high': data['high'].to_numpy(),
                        'low': data['low'].to_numpy(),
                        'close': data['close'].to_numpy(),
                        'volume': data['volume'].to_numpy(),
                        'close_time': [datetime.timestamp(i)*1000 for i in list(data['close_time'])]}
        print('data retrieved')
    except Exception as e:
        print(e)
        print('did not managed to get data from yfin')
        inputs=0
    return inputs

"""
Function name: get_data_yfinance
Description: This function is used to retrieve historical stock data from the yfinance library.
Inputs:
STOCK_ID (string): The stock symbol or ID of the stock for which data should be retrieved.
START_DATE (string): The start date for the historical data in the format 'YYYY-MM-DD'.
END_DATE (string): The end date for the historical data in the format 'YYYY-MM-DD'.
TIME_INTERVAL (string): The interval at which the data should be retrieved. Accepted
values include '1d', '1mo', '1y' etc.
Outputs:
inputs (dictionary): A dictionary containing historical data for the stock such as
open, high, low, close, volume and close_time.
Called functions: yf.download()
"""

# def get_data_yfinance(STOCK_ID,START_DATE,END_DATE,TIME_INTERVAL):
#     try:
#         data = yf.download(STOCK_ID, start=START_DATE, end=END_DATE, interval = TIME_INTERVAL)

#         inputs = {  'open': data['Open'].to_numpy(),
#                     'high': data['High'].to_numpy(),
#                     'low': data['Low'].to_numpy(),
#                     'close': data['Close'].to_numpy(),
#                     'volume': data['Volume'].to_numpy(),
#                     'close_time': data.index.to_numpy()}
#         print('data retrieved')
#     except Exception as e:
#             print('did not managed to get data from yfinance')
#             inputs=0
#     return inputs

def get_data_yfinance(STOCK_ID,START_DATE,END_DATE,TIME_INTERVAL):
    try:
        data = yf.download(STOCK_ID, start=START_DATE, end=END_DATE, interval = TIME_INTERVAL)
        if TIME_INTERVAL == '1d':
            data['close_time'] = data.index
            data['close_time'] = pd.to_datetime(data['close_time'])
            data['close_time'] = data['close_time'].astype(int) / 10**6
        if TIME_INTERVAL == '1h':
            data['close_time'] = data.index
            data['close_time'] = pd.to_datetime(data['close_time'], format='%Y-%m-%d %H:%M:%S%z')
            data['close_time'] = data['close_time'].dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
            data['close_time'] = data['close_time'].astype('datetime64[ns]')
            data['close_time'] = pd.to_datetime(data['close_time'])
            data['close_time'] = data['close_time'].astype(int) / 10**6
        inputs = {  'open': data['Open'].to_numpy(),
                    'high': data['High'].to_numpy(),
                    'low': data['Low'].to_numpy(),
                    'close': data['Close'].to_numpy(),
                    'volume': data['Volume'].to_numpy(),
                    'close_time': data['close_time'].to_numpy()}
        print('data retrieved')
    except Exception as e:
            print('did not managed to get data from yfinance',e)
            inputs=0
    return inputs
