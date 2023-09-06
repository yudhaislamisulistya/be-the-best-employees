from sqlalchemy import Column, Integer, String
from app.config.database import Base

class Employee(Base):
    __tablename__ = "employees"
    employee_id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String, unique=True, index=True)
    name = Column(String)
    description = Column(String)
    def as_dict_employee(self):
        return {
            "employee_id": self.employee_id,
            "employee_code": self.employee_code,
            "name": self.name,
            "description": self.description
        }