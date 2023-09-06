from typing import Union
from pydantic import BaseModel

class User(BaseModel):
    user_id: Union[int, None] = None
    username: str
    password: str
    name: str
    position: str
    role: int
    weight: int

    class Config:
        from_attributes = True

class Login(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True