import json
from fastapi import APIRouter
from util.ask_gpt import ask_GPT

router = APIRouter()

@router.get("/yperformance")
# /yperformance?symbol=aapl
async def historic():
    try:
        allo = ask_GPT("hello gpt how are you")
        print(allo)
        res = {"allo": allo}
        res = json.dumps(res)
    except Exception as e:
        res = 'error :' + str(e)
    return res
