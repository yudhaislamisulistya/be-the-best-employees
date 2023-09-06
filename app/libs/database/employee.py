from sqlalchemy.orm import Session
import app.models.employee as employee_model

def get_employee_by_code(db: Session, code: str):
    return db.query(employee_model.Employee).filter(employee_model.Employee.employee_code == code).first()

def get_employee_by_id(db: Session, employee_id: int):
    return db.query(employee_model.Employee).filter(employee_model.Employee.employee_id == employee_id).first()

def get_employees(db: Session, skip: int = 0, limit: int = 1000):
    results = db.query(employee_model.Employee).order_by(employee_model.Employee.employee_id.asc()).offset(skip).limit(limit).all()
    return results

def create_employee(db: Session, employee: employee_model.Employee):
    db_employee = employee_model.Employee(
        employee_code=employee.employee_code,
        name=employee.name,
        description=employee.description,
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee_by_id(db: Session, employee_id: int, employee: employee_model.Employee):
    db_employee = db.query(employee_model.Employee).filter(employee_model.Employee.employee_id == employee_id).first()
    db_employee.employee_code = employee.employee_code
    db_employee.name = employee.name
    db_employee.description = employee.description
    db.commit()
    db.refresh(db_employee)
    return db_employee

def delete_employee_by_id(db: Session, employee_id: int):
    db_employee = db.query(employee_model.Employee).filter(employee_model.Employee.employee_id == employee_id).first()
    db.delete(db_employee)
    db.commit()
    return db_employee