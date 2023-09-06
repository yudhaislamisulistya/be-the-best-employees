from typing import Union
from pydantic import BaseModel

class SubParameter(BaseModel):
    sub_parameter_id: Union[int, None] = None
    sub_parameter_code: str
    parameter_code: str
    name: str
    weight: int
    preference_type: str
    target: str
    q: Union[float, None] = None
    p: Union[float, None] = None
    
    class Config:
        from_attributes = True
