from sqlalchemy.orm import Session, subqueryload
import app.models.parameter as parameter_model
import app.models.sub_parameter as sub_parameter_model

def get_parameter_by_code(db: Session, code: str):
    return db.query(parameter_model.Parameter).filter(parameter_model.Parameter.parameter_code == code).first()

def get_parameter_by_id(db: Session, parameter_id: int):
    return db.query(parameter_model.Parameter).filter(parameter_model.Parameter.parameter_id == parameter_id).first()

def get_parameters(db: Session, skip: int = 0, limit: int = 1000):
    results = db.query(parameter_model.Parameter).order_by(parameter_model.Parameter.parameter_id.asc()).offset(skip).limit(limit).all()
    return results

def get_parameters_relation_sub_parameters(db: Session, skip: int = 0, limit: int = 1000):
    results = db.query(
        parameter_model.Parameter.parameter_id.label("parameter_id"),
        parameter_model.Parameter.parameter_code.label("parameter_code"),
        parameter_model.Parameter.name.label("parameter_name"),
        parameter_model.Parameter.weight.label("parameter_weight"),
        sub_parameter_model.SubParameter.sub_parameter_id.label("sub_parameter_id"),
        sub_parameter_model.SubParameter.sub_parameter_code.label("sub_parameter_code"),
        sub_parameter_model.SubParameter.name.label("sub_parameter_name"),
        sub_parameter_model.SubParameter.weight.label("sub_parameter_weight"),
        sub_parameter_model.SubParameter.preference_type.label("sub_parameter_preference_type"),
        sub_parameter_model.SubParameter.target.label("sub_parameter_target"),
        sub_parameter_model.SubParameter.q.label("sub_parameter_q"),
        sub_parameter_model.SubParameter.p.label("sub_parameter_p"),
    ).join(sub_parameter_model.SubParameter, parameter_model.Parameter.parameter_code == sub_parameter_model.SubParameter.parameter_code). \
    offset(skip).limit(limit).all()
    
    return results

def create_parameter(db: Session, parameter: parameter_model.Parameter):
    db_parameter = parameter_model.Parameter(
        parameter_code=parameter.parameter_code,
        name=parameter.name,
        weight=parameter.weight
    )
    db.add(db_parameter)
    db.commit()
    db.refresh(db_parameter)
    return db_parameter

def update_parameter_by_id(db: Session, parameter_id: int, parameter: parameter_model.Parameter):
    db_parameter = db.query(parameter_model.Parameter).filter(parameter_model.Parameter.parameter_id == parameter_id).first()
    db_parameter.parameter_code = parameter.parameter_code
    db_parameter.name = parameter.name
    db_parameter.weight = parameter.weight
    db.commit()
    db.refresh(db_parameter)
    return db_parameter

def delete_parameter_by_id(db: Session, parameter_id: int):
    db_parameter = db.query(parameter_model.Parameter).filter(parameter_model.Parameter.parameter_id == parameter_id).first()
    db.delete(db_parameter)
    db.commit()
    return db_parameter