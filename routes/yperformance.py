import numpy as np
import json

from fastapi import APIRouter
from util.market_data import historical_data_gmd
from util.calculate_return import calculate_return
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/yperformance")
# /yperformance?symbol=aapl
async def historic(symbol: str):
    try:
        today = datetime.now().date()
        one_year_ago = today - timedelta(days=365)
        start_date = one_year_ago.strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
        data = historical_data_gmd(symbol, start_date, end_date,"1d")
        starting_price = data['close'][0]
        final_price = data['close'][-1]
        res = {symbol: calculate_return(starting_price, final_price)}
        res = json.dumps(res)
    except Exception as e:
        res = 'error :' + str(e)
    return res
