from typing import Union
from pydantic import BaseModel

class Ranking(BaseModel):
    ranking_id: Union[int, None] = None
    user_id: int
    batch_code: str
    employee_code: str
    name: str
    net_flow: float
    ranking: int

    class Config:
        from_attributes = True
