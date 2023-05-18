from fastapi import APIRouter
from models.Indicator_request import Indicator_Request as Request

router = APIRouter()

@router.post("/engine/{strategy_id}")
async def run_engine(indicators: Request):
    pass