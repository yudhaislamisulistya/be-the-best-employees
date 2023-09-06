from sqlalchemy import Column, Integer, String
from app.config.database import Base

class Parameter(Base):
    __tablename__ = "parameters"
    parameter_id = Column(Integer, primary_key=True, index=True)
    parameter_code = Column(String, unique=True, index=True)
    name = Column(String)
    weight = Column(Integer)
    
    def __init__(self, parameter_id = None, parameter_code = None, name = None, weight = None, result_string = None, result_float = None):
        self.parameter_id = parameter_id
        self.parameter_code = parameter_code
        self.name = name
        self.weight = weight
        self.result_string = result_string
        self.result_float = result_float
    
    def as_dict_parameter(self):
        return {
            "parameter_id": self.parameter_id,
            "parameter_code": self.parameter_code,
            "name": self.name,
            "weight": self.weight,
            "result_string": self.result_string,
            "result_float": self.result_float 
        }
    
    def as_dict_default_parameter(self):
        return {
            "parameter_id": self.parameter_id,
            "parameter_code": self.parameter_code,
            "name": self.name,
            "weight": self.weight,
        }