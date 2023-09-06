from typing import Union
from pydantic import BaseModel

class PreferenceType(BaseModel):
    preference_type_id: Union[int, None] = None
    name: str
    type: str

    class Config:
        from_attributes = True
