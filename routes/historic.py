import numpy as np
import json

from fastapi import APIRouter
from market_data import historical_data_gmd
from fastapi_cache.decorator import cache

router = APIRouter()

@cache(expire=60)
@router.get("/historic")
# /historic?symbol=aapl&start_date=2022-01-06&end_date=2022-01-12&interval=1d
async def historic(symbol: str, start_date: str, end_date: str, interval: str):
    # for demonstration purposes, this is a slow endpoint that waits 5 seconds
    try:
        res = historical_data_gmd(symbol, start_date, end_date, interval)
        for key, value in res.items():
            if isinstance(value, np.ndarray):
                res[key] = value.tolist()

        # Convert the dictionary to a JSON-formatted string
        res = json.dumps(res)
    except Exception as e:
        res = 'error :' + str(e)
    return res
