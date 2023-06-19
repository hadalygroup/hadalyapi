import json

import json
from fastapi import APIRouter
from models.Report_request import report_request

router = APIRouter()

@router.post("/reports")
async def getIndicators(req: report_request):
    res = {}
    
    try:
        pass
    except Exception as e:
        pass
    return res

