import numpy as np
import json
import talib

from fastapi import APIRouter
from market_data import historical_data_gmd
from fastapi_cache.decorator import cache

router = APIRouter()

@router.get("/pattern")
# /pattern?symbol=aapl&start_date=2022-01-06&end_date=2022-01-12&interval=1d&pattern=CDL2CROWS
async def find_patterns(symbol: str, start_date: str, end_date: str, interval: str, pattern: str):
    # for demonstration purposes, this is a slow endpoint that waits 5 seconds
    try:
        res = historical_data_gmd(symbol, start_date, end_date, interval)
        for key, value in res.items():
            if isinstance(value, np.ndarray):
                res[key] = value
        pattern_function = getattr(talib, pattern)
        patterns = pattern_function(res['open'], res['high'], res['low'], res['close'])
        # Convert the dictionary to a JSON-formatted string

        res = json.dumps(patterns.tolist())
    except Exception as e:
        res = 'error :' + str(e)
    return res

