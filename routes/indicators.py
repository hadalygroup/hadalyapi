import numpy as np
import json
import logging

from fastapi import APIRouter
from util.market_data import historical_data_gmd
from models.Request import Request
router = APIRouter()

from talib import abstract
import numpy as np
from util.get_value_at_time import get_value_at_time

def calculate_indicators(inputs, ind_to_calculate: str, ADOSC_fastperiod = 3, ADOSC_slowperiod = 10):
    # ind=str(list(ind_to_calculate.keys())[0])s
    #i=ind_to_calculate[ind]

    Func = abstract.Function(ind_to_calculate)
    real = Func(inputs)
    #real = get_value_at_time(i['time'],real)
    return real

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
@router.get("/indicators")
async def get_indicators(indicators: Request):
    res = {}
    try:
        stock_data = historical_data_gmd(STOCK_ID=indicators.symbol, START_DATE=indicators.start_date, END_DATE=indicators.end_date, TIME_INTERVAL=indicators.interval)

        for indicator in indicators.indicators:
            indicator_value = calculate_indicators(stock_data,indicator)
            res[indicator] = indicator_value.tolist()

        res = json.dumps(res)
    except Exception as e:
        res = 'error :' + str(e)
    return res

