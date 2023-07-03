import json
from fastapi import APIRouter
from models.Strategy_request import Strategy_Request
from engine.strategy import Strategy
from engine.engine import Hadaly_Engine

router = APIRouter()

@router.post("/engine")
async def run_engine(req: Strategy_Request):
    try:
        strategy = Strategy(req.strategy, cash_wallet=req.cash_money, stock_wallet=req.stock_money)
        start_date = req.start_date
        end_date = req.end_date
        engine = Hadaly_Engine(strategy, req.stock, start_date, end_date,"1d")
        res = json.dumps(engine.simulation)
    except Exception as e:
        res = "error : " + str(e)
    return res

