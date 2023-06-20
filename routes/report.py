import json

import json
from fastapi import APIRouter
from models.Report_request import report_request

router = APIRouter()

@router.post("/reports")
async def getIndicators(req: report_request):
    res = {}
    portfolio = {}
    for index, action in enumerate(req.stocks):
        portfolio[action] = req.n_stocks[index]
    try:
        pass
    except Exception as e:
        pass
    return res

