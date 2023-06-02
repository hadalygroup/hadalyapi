from pydantic import BaseModel

class Strategy_Request(BaseModel):
    strategy: str
    stock: str
    start_date: str
    end_date: str