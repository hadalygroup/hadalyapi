import numpy as np
import json
import talib

from fastapi import APIRouter
from market_data import historical_data_gmd
from fastapi_cache.decorator import cache

router = APIRouter()

"""
Function name: find_patterns

Description: Retrives data returns if the pattern has been found

Inputs
    symbol: string, stock symbol (e.g. Apple -> aapl)
    start_date: string, the start date of the data in the format 'YYYY-MM-DD'
    end_date: string, the end date of the data in the format 'YYYY-MM-DD'
    interval: string, the time interval of the data (e.g. '1d' for daily data)
    pattern: string, refering to a candle stick pattern (e.g. CDL2CROWS = Two crows pattern)
    
Output:
    List composed of 4 integers (1 if pattern exists, 0 if not) -> [open, high, low, close]

Called functions:
    historical_data_gmd(symbol, start_date, end_date, interval)
    """
@router.get("/pattern")
# /pattern?symbol=aapl&start_date=2022-01-06&end_date=2022-01-12&interval=1d&pattern=CDL2CROWS

async def find_patterns(symbol: str, start_date: str, end_date: str, interval: str, pattern: str):
    # for demonstration purposes, this is a slow endpoint that waits 5 seconds
    try:
        res = historical_data_gmd(symbol, start_date, end_date, interval)
        for key, value in res.items():
            if isinstance(value, np.ndarray):
                res[key] = value
        pattern_function = getattr(talib, pattern) #talib.CDL2CROWS
        patterns = pattern_function(res['open'], res['high'], res['low'], res['close'])
        # Convert the dictionary to a JSON-formatted string

        res = json.dumps(patterns.tolist())
    except Exception as e:
        res = 'error :' + str(e)
    return res

