import asyncio

from fastapi import APIRouter
from models.user import UserResponse
from fastapi_cache.decorator import cache

router = APIRouter()

@cache(expire=30)  # cache for 30 seconds
@router.get("/cached", response_model=UserResponse)
async def cached():
    # for demonstration purposes, this is a slow endpoint that waits 5 seconds
    await asyncio.sleep(5)
    print("hello world")
    return {
        "user_id": "0123456789",
        "email": "cached@kylegill.com",
        "name": "Kyle Gill",
    }