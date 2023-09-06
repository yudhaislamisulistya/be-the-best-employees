from sqlalchemy import Column, Integer, String
from app.config.database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String)
    position = Column(String)
    role = Column(Integer)
    weight = Column(Integer)
    def as_dict_user(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "name": self.name,
            "position": self.position,
            "role": self.role,
            "weight": self.weight
        }