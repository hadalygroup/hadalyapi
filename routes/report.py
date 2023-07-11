import json
from fastapi import APIRouter, BackgroundTasks
from models.Report_request import report_request as Request
from reports.generate_report import generate_report

router = APIRouter()

@router.post("/report")
async def getIndicators(req: Request, backgroud_task: BackgroundTasks):
    backgroud_task.add_task(generate_report, req.portfolio)
    return {"message": "started"}

