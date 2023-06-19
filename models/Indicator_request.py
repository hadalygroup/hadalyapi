from typing import List, Union
from pydantic import BaseModel


class Indicator_Request(BaseModel):
    indicators: List[Union[dict, str]]
    symbol: str
    start_date: str
    end_date: str
    interval: str

    #symbol: str, start_date: str, end_date: str, interval: str, pattern: str