from typing import Union
from pydantic import BaseModel

class Parameter(BaseModel):
    parameter_id: Union[int, None] = None
    parameter_code: str
    name: str
    weight: int

    class Config:
        from_attributes = True
