import json

import yfinance as yf
from fastapi import APIRouter
import datetime

router = APIRouter()

def calculateSPXReturn():
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=365)

    sp500_data = yf.download('^GSPC', start=start_date, end=end_date, progress=False)
    sp500_return = (sp500_data['Close'][-1] - sp500_data['Close'][0]) / sp500_data['Close'][0] * 100
    return round(sp500_return,4)

@router.get("/GSPC")
# /yperformance?symbol=aapl
async def historic():
    try:
        sp500_return = calculateSPXReturn()
        res = {"GSPC": sp500_return}
        res = json.dumps(res)
    except Exception as e:
        res = 'error :' + str(e)
    return res