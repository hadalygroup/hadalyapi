import json
from fastapi import APIRouter
from models.Report_request import report_request
import yfinance as yf
router = APIRouter()

@router.post("/reports")
async def getIndicators(req: report_request):
    res = {}
    portfolio = {}

    for index, action in enumerate(req.stocks):
        portfolio[action] = req.n_stocks[index]
    for stock, amount in portfolio.items():
        stock = yf.ticker(stock)
        pass

    try:
        pass
    except Exception as e:
        pass
    return res

