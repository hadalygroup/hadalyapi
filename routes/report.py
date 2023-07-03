import json
from reports.generate_content import generate_report
from fastapi import APIRouter
from models.Report_request import report_request as Request


router = APIRouter()

@router.post("/report")
async def getIndicators(req: Request):
    res = {}
    
    try:
        print(generate_report())
        res["allo": generate_report()]
        res = json.dumps(res)
    except Exception as e:
        res = 'error :' + str(e)
    return res

