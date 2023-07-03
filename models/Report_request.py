from pydantic import BaseModel
from typing import List

class report_request(BaseModel):
    stocks: List[str]
    n_stocks: List[int]
    email = str