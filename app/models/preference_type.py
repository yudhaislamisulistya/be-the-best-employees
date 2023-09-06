from sqlalchemy import Column, Integer, String, Float
from app.config.database import Base

class PreferenceType(Base):
    __tablename__ = "preference_types"
    preference_type_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    
    def __init__(self, preference_type_id = None, name = None, type = None):
        self.preference_type_id = preference_type_id
        self.name = name
        self.type = type
        
    def as_dict_default_preference_type(self):
        return {
            "preference_type_id": self.preference_type_id,
            "name": self.name,
            "type": self.type,
        }