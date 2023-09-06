from sqlalchemy import Column, Integer, String
from app.config.database import Base

class Batch(Base):
    __tablename__ = "batchs"
    batch_id = Column(Integer, primary_key=True, index=True)
    batch_code = Column(String, unique=True, index=True)
    name = Column(String)
    description = Column(String)
    def as_dict_batch(self):
        return {
            "batch_id": self.batch_id,
            "batch_code": self.batch_code,
            "name": self.name,
            "description": self.description
        }