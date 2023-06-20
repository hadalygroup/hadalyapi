import numpy as np
import json

from fastapi import APIRouter
from util.market_data import historical_data_gmd
from models.Indicator_request import Indicator_Request as Request
from util.calculateIndicators import calculateIndicators
import json
import numpy as np

router = APIRouter()


"""
Function name: get_indicators

Description: Retrives data returns if the indicators have been found

Input:
    {
        "end_date": "2023-6-5",
        "indicators": ["RSI",{"indicator": "MIDPRICE", "params": {"time": 13}, "id":"ab"}],
        "interval": "1d",
        "start_date": "2022-6-5",
        "symbol": "AAPL"
    }
    
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

        indicators_values = calculateIndicators(stock_data, indicators_list)
        for i in range(len(indicators_values)):
            key = indicators_list[i]
            if isinstance(key, dict):
                res[key["id"]] = indicators_values[i]
                continue
            res[key] = indicators_values[i]
        res = {"dates": stock_data['close'].tolist(), "indicators": res}
        res = json.dumps(res)
    except Exception as e:
        res = 'error :' + str(e)
    return res

