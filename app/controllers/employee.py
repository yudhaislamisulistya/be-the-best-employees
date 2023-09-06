from sqlalchemy.orm import Session
import app.libs.database.employee as employee_db
import app.schemas.employee as schema_employee

class EmployeeController:
    def get_employees(self, db: Session, skip: int = 0, limit: int = 1000):
        employees = employee_db.get_employees(db=db, skip=skip, limit=limit)
        
        return employees or []
    def create_employee(self, db: Session, employee=schema_employee.Employee):
        data = employee_db.get_employee_by_code(db=db, code=employee.employee_code)
        if data:
            return False
        
        return employee_db.create_employee(db=db, employee=employee)
    def update_employee(self, db: Session, employee_id=int, employee=schema_employee.Employee):
        dataEmployeeById = employee_db.get_employee_by_id(db=db, employee_id=employee_id)
        if not dataEmployeeById:
            return 404
        
        dataEmployeeByCode = employee_db.get_employee_by_code(db=db, code=employee.employee_code)
        if dataEmployeeByCode and dataEmployeeByCode.employee_id != employee_id:
            return 409
        
        return employee_db.update_employee_by_id(db=db, employee_id=employee_id, employee=employee)
    def delete_employee(self, db: Session, employee_id=int):
        dataEmployeeById = employee_db.get_employee_by_id(db=db, employee_id=employee_id)
        if not dataEmployeeById:
            return 404
        
        return employee_db.delete_employee_by_id(db=db, employee_id=employee_id)