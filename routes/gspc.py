import json

import yfinance as yf
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

def calculateSPXReturn():
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=365)

    sp500_data = yf.download('^GSPC', start=start_date, end=end_date, progress=False)
    sp500_return = (sp500_data['Close'][-1] - sp500_data['Close'][0]) / sp500_data['Close'][0] * 100
    return sp500_return

@router.get("/GSPC")
# /yperformance?symbol=aapl
async def historic():
    try:
        res = {"GSPC": calculateSPXReturn()}
        res = json.dumps(res)
    except Exception as e:
        res = 'error :' + str(e)
    return res
