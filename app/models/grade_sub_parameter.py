from sqlalchemy import Column, Integer, String
from app.config.database import Base

class GradeSubParameter(Base):
    __tablename__ = "grade_sub_parameters"
    grade_sub_parameter_id = Column(Integer, primary_key=True, index=True)
    sub_parameter_code = Column(String)
    description = Column(String)
    weight = Column(Integer)
    
    def as_dict_grade_sub_parameter(self):
        return {
            "grade_sub_parameter_id": self.grade_sub_parameter_id,
            "sub_parameter_code": self.sub_parameter_code,
            "description": self.description,
            "weight": self.weight
        } 