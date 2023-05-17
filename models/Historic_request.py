from typing import List
from pydantic import BaseModel


class Historic_request(BaseModel):
    symbol: str
    start_date: str
    end_date: str
    interval: str

    #symbol: str, start_date: str, end_date: str, interval: str, pattern: str