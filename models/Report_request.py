from pydantic import BaseModel

class report_request(BaseModel):
    portfolio: dict
    email: str