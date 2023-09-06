from sqlalchemy.orm import Session
import app.libs.database.grade_sub_parameter as grade_sub_parameter_db
import app.schemas.grade_sub_parameter as schema_grade_sub_parameter

class GradeSubParameterController:
    def get_grade_sub_parameters(self, db: Session, skip: int = 0, limit: int = 1000):
        grade_sub_parameters = grade_sub_parameter_db.get_grade_sub_parameters(db=db, skip=skip, limit=limit)
        
        return grade_sub_parameters or []
    
    def create_grade_sub_parameter(self, db: Session, grade_sub_parameter=schema_grade_sub_parameter.GradeSubParameter):
        return grade_sub_parameter_db.create_grade_sub_parameter(db=db, grade_sub_parameter=grade_sub_parameter)
    
    def update_grade_sub_parameter(self, db: Session, grade_sub_parameter_id=int, grade_sub_parameter=schema_grade_sub_parameter.GradeSubParameter):
        GradedataSubParameterById = grade_sub_parameter_db.get_grade_sub_parameter_by_id(db=db, grade_sub_parameter_id=grade_sub_parameter_id)
        if not GradedataSubParameterById:
            return 404
        
        return grade_sub_parameter_db.update_grade_sub_parameter_by_id(db=db, grade_sub_parameter_id=grade_sub_parameter_id, grade_sub_parameter=grade_sub_parameter)
    
    def delete_grade_sub_parameter(self, db: Session, grade_sub_parameter_id=int):
        GradedataSubParameterById = grade_sub_parameter_db.get_grade_sub_parameter_by_id(db=db, grade_sub_parameter_id=grade_sub_parameter_id)
        if not GradedataSubParameterById:
            return 404
        
        return grade_sub_parameter_db.delete_grade_sub_parameter_by_id(db=db, grade_sub_parameter_id=grade_sub_parameter_id)