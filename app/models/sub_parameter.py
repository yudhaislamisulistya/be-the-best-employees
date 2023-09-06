from sqlalchemy import Column, Integer, String, Float
from app.config.database import Base

class SubParameter(Base):
    __tablename__ = "sub_parameters"
    sub_parameter_id = Column(Integer, primary_key=True, index=True)
    sub_parameter_code = Column(String, unique=True, index=True)
    parameter_code = Column(String)
    name = Column(String)
    weight = Column(Integer)
    preference_type = Column(String)
    target = Column(String)
    q = Column(Float)
    p = Column(Float)
    
    def __init__(self, sub_parameter_id = None, sub_parameter_code = None, parameter_code = None, name = None, weight = None, result_string=None, result_float=None, preference_type = None, target = None, q = None, p = None):
        self.sub_parameter_id = sub_parameter_id
        self.sub_parameter_code = sub_parameter_code
        self.parameter_code = parameter_code
        self.name = name
        self.weight = weight
        self.result_string = result_string 
        self.result_float = result_float 
        self.preference_type = preference_type
        self.target = target
        self.q = q
        self.p = p
    
    def as_dict_sub_parameter(self):
        return {
            "sub_parameter_id": self.sub_parameter_id,
            "sub_parameter_code": self.sub_parameter_code,
            "parameter_code": self.parameter_code,
            "name": self.name,
            "weight": self.weight,
            "result_string": self.result_string,
            "result_float": self.result_float,
            "preference_type": self.preference_type,
            "target": self.target,
            "q": self.q,
            "p": self.p,
        }
    
    def as_dict_default_sub_parameter(self):
        return {
            "sub_parameter_id": self.sub_parameter_id,
            "sub_parameter_code": self.sub_parameter_code,
            "parameter_code": self.parameter_code,
            "name": self.name,
            "weight": self.weight,
            "preference_type": self.preference_type,
            "target": self.target,
            "q": self.q,
            "p": self.p,
        }