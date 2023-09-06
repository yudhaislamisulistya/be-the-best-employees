from sqlalchemy.orm import Session
from sqlalchemy import bindparam
import app.models.sub_parameter_employee as sub_parameter_employee_model
from sqlalchemy.dialects.postgresql import insert

def get_sub_parameter_employee_by_code(db: Session, code: str):
    return db.query(sub_parameter_employee_model.SubParameterEmployee).filter(sub_parameter_employee_model.SubParameterEmployee.grade_sub_sub_parameter_code == code).first()

def get_sub_parameter_employee_by_id(db: Session, sub_parameter_employee_id: int):
    return db.query(sub_parameter_employee_model.SubParameterEmployee).filter(sub_parameter_employee_model.SubParameterEmployee.sub_parameter_employee_id == sub_parameter_employee_id).first()

def get_sub_parameter_employees(db: Session, skip: int = 0, limit: int = 1000):
    results = db.query(sub_parameter_employee_model.SubParameterEmployee).offset(skip).limit(limit).all()
    return results

def get_sub_parameter_employee_by_code_and_user_id(db: Session, skip: int = 0, limit: int = 1000, sub_parameter_employee_code: str = None, user_id: int = None):
    results = db.query(sub_parameter_employee_model.SubParameterEmployee).filter(sub_parameter_employee_model.SubParameterEmployee.sub_parameter_employee_code == sub_parameter_employee_code, sub_parameter_employee_model.SubParameterEmployee.user_id == user_id).offset(skip).limit(limit).all()
    return results

def create_sub_parameter_employee(db: Session, sub_parameter_employee: sub_parameter_employee_model.SubParameterEmployee):
    db_sub_parameter_employee = sub_parameter_employee_model.SubParameterEmployee(
        sub_parameter_employee_code=sub_parameter_employee.sub_parameter_employee_code,
        employee_code=sub_parameter_employee.employee_code,
        sub_parameter_code=sub_parameter_employee.sub_parameter_code,
        value=sub_parameter_employee.value
    )
    db.add(db_sub_parameter_employee)
    db.commit()
    db.refresh(db_sub_parameter_employee)
    return db_sub_parameter_employee

def bulk_create_sub_parameter_employee(db: Session, sub_parameter_employees: list):
    db.execute(sub_parameter_employee_model.SubParameterEmployee.__table__.insert(), sub_parameter_employees)
    db.commit()
    return sub_parameter_employees

def bulk_update_sub_parameter_employee(db: Session, sub_parameter_employees: list):
    upsert_stmt = insert(sub_parameter_employee_model.SubParameterEmployee).values(sub_parameter_employees)
    upsert_stmt = upsert_stmt.on_conflict_do_update(
        index_elements=[sub_parameter_employee_model.SubParameterEmployee.sub_parameter_employee_id],
        set_={
            "sub_parameter_employee_code": upsert_stmt.excluded.sub_parameter_employee_code,
            "employee_code": upsert_stmt.excluded.employee_code,
            "sub_parameter_code": upsert_stmt.excluded.sub_parameter_code,
            "value": upsert_stmt.excluded.value
        }
    )
    db.execute(upsert_stmt)
    db.commit()
    return sub_parameter_employees

def update_sub_parameter_employee_by_id(db: Session, sub_parameter_employee_id: int, sub_parameter_employee: sub_parameter_employee_model.SubParameterEmployee):
    db_sub_parameter_employee = db.query(sub_parameter_employee_model.SubParameterEmployee).filter(sub_parameter_employee_model.SubParameterEmployee.sub_parameter_employee_id == sub_parameter_employee_id).first()
    db_sub_parameter_employee.sub_parameter_employee_code = sub_parameter_employee.sub_parameter_employee_code
    db_sub_parameter_employee.employee_code = sub_parameter_employee.employee_code
    db_sub_parameter_employee.sub_parameter_code = sub_parameter_employee.sub_parameter_code
    db_sub_parameter_employee.value = sub_parameter_employee.value
    db.commit()
    db.refresh(db_sub_parameter_employee)
    return db_sub_parameter_employee

def delete_sub_parameter_employee_by_id(db: Session, sub_parameter_employee_id: int):
    db_sub_parameter_employee = db.query(sub_parameter_employee_model.SubParameterEmployee).filter(sub_parameter_employee_model.SubParameterEmployee.sub_parameter_employee_id == sub_parameter_employee_id).first()
    db.delete(db_sub_parameter_employee)
    db.commit()
    return db_sub_parameter_employee

def delete_sub_parameter_employees_by_code(db: Session, sub_parameter_employee_code: str):
    db.query(sub_parameter_employee_model.SubParameterEmployee).filter(sub_parameter_employee_model.SubParameterEmployee.sub_parameter_employee_code == sub_parameter_employee_code).delete()
    db.commit()
    return True