from pydantic import BaseModel

class UserResponse(BaseModel):
    user_id: str
    email: str
    name: str