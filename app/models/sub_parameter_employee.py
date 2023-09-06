from sqlalchemy import Column, Integer, String
from app.config.database import Base

class SubParameterEmployee(Base):
    __tablename__ = "sub_parameter_employees"
    sub_parameter_employee_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    sub_parameter_employee_code = Column(String)
    employee_code = Column(String)
    sub_parameter_code = Column(String)
    value = Column(Integer)
    
    def __init__(self, sub_parameter_employee_id = None, user_id = None, sub_parameter_employee_code = None, employee_code = None, sub_parameter_code = None, value = None):
        self.sub_parameter_employee_id = sub_parameter_employee_id
        self.user_id = user_id
        self.sub_parameter_employee_code = sub_parameter_employee_code
        self.employee_code = employee_code
        self.sub_parameter_code = sub_parameter_code
        self.value = value
    
    
    def as_dict_default_sub_parameter_employee(self):
        return {
            "sub_parameter_employee_id": self.sub_parameter_employee_id,
            "user_id": self.user_id,
            "sub_parameter_employee_code": self.sub_parameter_employee_code,
            "employee_code": self.employee_code,
            "sub_parameter_code": self.sub_parameter_code,
            "value": self.value
        }