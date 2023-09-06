from sqlalchemy.orm import Session
import app.models.grade_sub_parameter as grade_sub_parameter_model

def get_grade_sub_parameter_by_code(db: Session, code: str):
    return db.query(grade_sub_parameter_model.GradeSubParameter).filter(grade_sub_parameter_model.GradeSubParameter.grade_sub_sub_parameter_code == code).first()

def get_grade_sub_parameter_by_id(db: Session, grade_sub_parameter_id: int):
    return db.query(grade_sub_parameter_model.GradeSubParameter).filter(grade_sub_parameter_model.GradeSubParameter.grade_sub_parameter_id == grade_sub_parameter_id).first()

def get_grade_sub_parameters(db: Session, skip: int = 0, limit: int = 1000):
    results = db.query(grade_sub_parameter_model.GradeSubParameter).offset(skip).limit(limit).all()
    return results

def create_grade_sub_parameter(db: Session, grade_sub_parameter: grade_sub_parameter_model.GradeSubParameter):
    db_grade_sub_parameter = grade_sub_parameter_model.GradeSubParameter(
        sub_parameter_code=grade_sub_parameter.sub_parameter_code,
        description=grade_sub_parameter.description,
        weight=grade_sub_parameter.weight
    )
    db.add(db_grade_sub_parameter)
    db.commit()
    db.refresh(db_grade_sub_parameter)
    return db_grade_sub_parameter

def update_grade_sub_parameter_by_id(db: Session, grade_sub_parameter_id: int, grade_sub_parameter: grade_sub_parameter_model.GradeSubParameter):
    db_grade_sub_parameter = db.query(grade_sub_parameter_model.GradeSubParameter).filter(grade_sub_parameter_model.GradeSubParameter.grade_sub_parameter_id == grade_sub_parameter_id).first()
    db_grade_sub_parameter.sub_parameter_code = grade_sub_parameter.sub_parameter_code
    db_grade_sub_parameter.description = grade_sub_parameter.description
    db_grade_sub_parameter.weight = grade_sub_parameter.weight
    db.commit()
    db.refresh(db_grade_sub_parameter)
    return db_grade_sub_parameter

def delete_grade_sub_parameter_by_id(db: Session, grade_sub_parameter_id: int):
    db_grade_sub_parameter = db.query(grade_sub_parameter_model.GradeSubParameter).filter(grade_sub_parameter_model.GradeSubParameter.grade_sub_parameter_id == grade_sub_parameter_id).first()
    db.delete(db_grade_sub_parameter)
    db.commit()
    return db_grade_sub_parameter