import logging
import subprocess
import time

import redis.asyncio as redis
import uvicorn
import openai
import os
from os.path import join, dirname
from dotenv import load_dotenv

from fastapi import Depends, FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi.middleware.cors import CORSMiddleware

from routes.user import router as user_router
from routes.root import router as root_router
from routes.historic import router as historic_router
from routes.cached import router as cache_router
from routes.indicators import router as indicator_router
from routes.engine import router as engine_router
from routes.yperformance import router as year_router

from config import settings

app = FastAPI(dependencies=[Depends(RateLimiter(times=10, seconds=5))])
logger = logging.getLogger(__name__)
# .env variables can be validated and accessed from the config, here to set a log level
logging.basicConfig(level=settings.LOG_LEVEL.upper())

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root_router)
app.include_router(user_router)
app.include_router(historic_router)
app.include_router(cache_router)
app.include_router(indicator_router)
app.include_router(engine_router)
app.include_router(year_router)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

key = os.environ.get("openai_key")
openai.organization = os.environ.get("openai_org")

openai.api_key = key
models = openai.Model.list()



@app.on_event("startup")
async def startup():
    redis_url = f"redis://default:SLTXD3Xogqt1PAu7tYts@containers-us-west-7.railway.app:6754"
    try:
        red = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
        await FastAPILimiter.init(red)
    except Exception:
        raise Exception(
            "Redis connection failed, ensure redis is running on the default port 6379"
        )

    FastAPICache.init(RedisBackend(red), prefix="fastapi-cache")


@app.middleware("http")
async def time_request(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["Server-Timing"] = str(process_time)
    logger.info(f"{request.method} {round(process_time, 5)}s {request.url}")
    return response


def dev():
    try:
        subprocess.check_output(["redis-cli", "ping"], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        logger.warning(
            "Redis is not already running, have you started it with redis-server?"
        )
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
