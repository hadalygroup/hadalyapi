from fastapi import APIRouter
from models.Indicator_request import Indicator_Request as Request
from models.Strategy_request import Strategy_Request
from engine.strategy import Strategy
from engine.engine import Hadaly_Engine
from datetime import datetime, timedelta
import json

router = APIRouter()

@router.post("/engine")
async def run_engine(req: Strategy_Request):
    try:
        strategy = Strategy(req.strategy, cash_wallet=req.money)
        start_date = req.start_date
        yesterday = datetime.now().date() - timedelta(days=1)
        end_date = req.end_date
        engine = Hadaly_Engine(strategy, req.stock, start_date, end_date,"1d")
        res = json.dumps(engine.simulation)
    except Exception as e:
        res = "error : " + str(e)
    return res

