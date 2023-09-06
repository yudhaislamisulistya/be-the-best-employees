from sqlalchemy.orm import Session
import app.models.sub_parameter as sub_parameter_model

def get_sub_parameter_by_code(db: Session, code: str):
    return db.query(sub_parameter_model.SubParameter).filter(sub_parameter_model.SubParameter.sub_parameter_code == code).first()

def get_sub_parameter_by_id(db: Session, sub_parameter_id: int):
    return db.query(sub_parameter_model.SubParameter).filter(sub_parameter_model.SubParameter.sub_parameter_id == sub_parameter_id).first()

def get_sub_parameters(db: Session, skip: int = 0, limit: int = 1000):
    results = db.query(sub_parameter_model.SubParameter).order_by(sub_parameter_model.SubParameter.sub_parameter_id.asc()).offset(skip).limit(limit).all()
    return results

def create_sub_parameter(db: Session, sub_parameter: sub_parameter_model.SubParameter):
    db_sub_parameter = sub_parameter_model.SubParameter(
        sub_parameter_code=sub_parameter.sub_parameter_code,
        parameter_code=sub_parameter.parameter_code,
        name=sub_parameter.name,
        weight=sub_parameter.weight,
        preference_type=sub_parameter.preference_type,
        target=sub_parameter.target,
        q=sub_parameter.q,
        p=sub_parameter.p,
    )
    db.add(db_sub_parameter)
    db.commit()
    db.refresh(db_sub_parameter)
    return db_sub_parameter

def update_sub_parameter_by_id(db: Session, sub_parameter_id: int, sub_parameter: sub_parameter_model.SubParameter):
    db_sub_parameter = db.query(sub_parameter_model.SubParameter).filter(sub_parameter_model.SubParameter.sub_parameter_id == sub_parameter_id).first()
    db_sub_parameter.sub_parameter_code = sub_parameter.sub_parameter_code
    db_sub_parameter.parameter_code = sub_parameter.parameter_code
    db_sub_parameter.name = sub_parameter.name
    db_sub_parameter.weight = sub_parameter.weight
    db_sub_parameter.preference_type = sub_parameter.preference_type
    db_sub_parameter.target = sub_parameter.target
    db_sub_parameter.q = sub_parameter.q
    db_sub_parameter.p = sub_parameter.p
    db.commit()
    db.refresh(db_sub_parameter)
    return db_sub_parameter

def delete_sub_parameter_by_id(db: Session, sub_parameter_id: int):
    db_sub_parameter = db.query(sub_parameter_model.SubParameter).filter(sub_parameter_model.SubParameter.sub_parameter_id == sub_parameter_id).first()
    db.delete(db_sub_parameter)
    db.commit()
    return db_sub_parameter