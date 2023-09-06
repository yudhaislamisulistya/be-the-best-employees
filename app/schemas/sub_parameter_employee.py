from typing import Union, Dict
from pydantic import BaseModel

class SubParameterEmployee(BaseModel):
    sub_parameter_employee_id: Union[int, None] = None
    user_id: int
    sub_parameter_employee_code: str
    employee_code: str
    sub_parameter_code: str
    value : int

    class Config:
        from_attributes = True