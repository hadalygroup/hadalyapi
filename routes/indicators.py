import numpy as np
import json
import logging

from fastapi import APIRouter
from util.market_data import historical_data_gmd
from models.indicator import Indicators
from util.calculate_indicator import calculate_indicators
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
@router.get("/indicators")
async def get_indicators(indicators: Indicators):
    logging.debug("heloge")
    res = {}
    try:
        OHLC_data = historical_data_gmd(STOCK_ID=indicators.symbol, START_DATE=indicators.start_date, END_DATE=indicators.end_date, TIME_INTERVAL=indicators.interval)
        for OHLC, value in OHLC_data.items():
            if isinstance(value, np.ndarray):
                OHLC_data[OHLC] = value
        for indicator in indicators.indicators:
            indicator_value = calculate_indicators(OHLC_data,indicator)
            res[indicator] = indicator_value.tolist()

        res = json.dumps(res)
    except Exception as e:
        res = 'error :' + str(e)
    return res

