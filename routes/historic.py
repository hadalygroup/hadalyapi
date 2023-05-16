import numpy as np
import json

from fastapi import APIRouter
from util.market_data import historical_data_gmd
from models.Historic_request import Historic_request

router = APIRouter()

@router.get("/historic")
# /historic?symbol=aapl&start_date=2022-01-06&end_date=2022-01-12&interval=1d
async def historic(request: Historic_request):
    try:
        res = historical_data_gmd(request.symbol, request.start_date, request.end_date, request.interval)
        for key, value in res.items():
            if isinstance(value, np.ndarray):
                res[key] = value.tolist()

        # Convert the dictionary to a JSON-formatted string
        print(res['open'])
        res = json.dumps(res)
    except Exception as e:
        res = 'error :' + str(e)
    return res
