from fastapi import APIRouter
from models.user import UserResponse

router = APIRouter()

@router.get("/user", response_model=UserResponse)
def current_user():
    # this endpoint's repsonse will match the UserResponse model
    return {
        "user_id": "0123456789",
        "email": "me@kylegill.com",
        "name": "Kyle Gill",
        "extra_field_ignored_by_model": "This field is ignored by the response model",
    }