from pydantic import BaseModel

class Strategy_Request(BaseModel):
    strategy: dict
    stock: str
    start_date: str
    end_date: str
    cash_money: int | None = None
    stock_money: int | None = None