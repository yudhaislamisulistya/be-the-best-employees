from typing import Union
from pydantic import BaseModel

class Batch(BaseModel):
    batch_id: Union[int, None] = None
    batch_code: str
    name: str
    description: Union[str, None] = None 

    class Config:
        from_attributes = True
