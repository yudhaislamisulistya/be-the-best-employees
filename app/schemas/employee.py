from typing import Union
from pydantic import BaseModel

class Employee(BaseModel):
    employee_id: Union[int, None] = None
    employee_code: str
    name: str
    description: Union[str, None] = None 

    class Config:
        from_attributes = True
