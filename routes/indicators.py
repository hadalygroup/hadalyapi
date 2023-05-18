import numpy as np
import json

from fastapi import APIRouter
from util.market_data import historical_data_gmd
from models.Indicator_request import Indicator_Request as Request
from util.calculateIndicators import calculateIndicators

from talib import abstract
import numpy as np

router = APIRouter()


"""
Function name: get_indicators

Description: Retrives data returns if the indicators have been found

Inputs
    indicator: type is Indicators => contains all the data needed
    
Output:
    Dictionnary where key = indicator name and value is a dictionnary corresponding to what was calculated by calculate_indicator

Called functions:
    historical_data_gmd(symbol, start_date, end_date, interval)
"""
@router.post("/indicators")
async def getIndicators(indicators: Request):
    res = {}
    
    try:
        indicators_list = indicators.indicators
     
        stock_data = historical_data_gmd(STOCK_ID=indicators.symbol, START_DATE=indicators.start_date, END_DATE=indicators.end_date, TIME_INTERVAL=indicators.interval)

        indicators_value = calculateIndicators(stock_data, indicators_list)

        for i in range(len(indicators_value)):
            res[indicators_list[i]] = indicators_value[i]

        res = {"dates": stock_data['close'].tolist(), "indicators": res}
        res = json.dumps(res)
    except Exception as e:
        res = 'error :' + str(e)
    return res

