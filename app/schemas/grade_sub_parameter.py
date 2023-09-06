from typing import Union
from pydantic import BaseModel

class GradeSubParameter(BaseModel):
    grade_sub_parameter_id: Union[int, None] = None
    sub_parameter_code: str
    description: str
    weight: int
    
    class Config:
        from_attributes = True
