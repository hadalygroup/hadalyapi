import json
from fastapi import APIRouter
from models.Report_request import report_request as Request
from reports.generate_report import generate_report

router = APIRouter()

@router.post("/report")
async def getIndicators(req: Request):
    res = {}
    generate_report(req.portfolio)
    # events = get_past_events()
    # imp_events = review_past_events({"JPM": 0.0784, "KO": 0.5359, "JNJ": 0.1067, "PG": 0.275, "VZ": 0.004})
    # if imp_events != None:
    #    for event in imp_events:
    #        print(event)
    #        print(event in events)
    try:
        # font_config = FontConfiguration()

        # HTML_text = generate_HTML()
        # css = CSS(filename="./reports/report.css")
        # html = HTML(string=HTML_text, base_url=".")
        # html.write_pdf(
        #     './example.pdf',
        #     stylesheets=[css],
        #     font_config=font_config
        # )

        res = json.dumps(res)
    except Exception as e:
        res = 'error :' + str(e)
    return res

