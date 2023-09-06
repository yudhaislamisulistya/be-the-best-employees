from sqlalchemy.orm import Session
import app.libs.database.batch as batch_db
import app.libs.database.sub_parameter_employee as sub_parameter_employee_db
import app.libs.database.employee as employee_db
import app.libs.database.sub_parameter as sub_parameter_db
import app.libs.database.sub_parameter_employee as sub_parameter_employee_db
import app.schemas.batch as schema_batch
import app.schemas.sub_parameter_employee as schema_sub_parameter_employee

class BatchController:
    def get_batchs(self, db: Session, skip: int = 0, limit: int = 1000):
        batchs = batch_db.get_batchs(db=db, skip=skip, limit=limit)
        
        return batchs or []
    def create_batch(self, db: Session, batch=schema_batch.Batch):
        data = batch_db.get_batch_by_code(db=db, code=batch.batch_code)
        if data:
            return False
        
        # make object from employee and sub_parameter loopoing
        dataEmployees = employee_db.get_employees(db=db, skip=0, limit=1000)
        dataSubParameters = sub_parameter_db.get_sub_parameters(db=db, skip=0, limit=1000)
        sub_parameter_employees = []
        for dataEmployee in dataEmployees:
            for dataSubParameter in dataSubParameters:
                sub_parameter_employees.append(schema_sub_parameter_employee.SubParameterEmployee(
                    user_id=2,
                    sub_parameter_employee_code=batch.batch_code,
                    employee_code=dataEmployee.employee_code,
                    sub_parameter_code=dataSubParameter.sub_parameter_code,
                    value=0
                ))
        sub_parameter_employees = [sub_parameter_employee.__dict__ for sub_parameter_employee in sub_parameter_employees]
        for sub_parameter_employee in sub_parameter_employees:
            del sub_parameter_employee['sub_parameter_employee_id']
        print(sub_parameter_employees)
        sub_parameter_employee_db.bulk_create_sub_parameter_employee(db=db, sub_parameter_employees=sub_parameter_employees)        
        return batch_db.create_batch(db=db, batch=batch)
    def update_batch(self, db: Session, batch_id=int, batch=schema_batch.Batch):
        dataBatchById = batch_db.get_batch_by_id(db=db, batch_id=batch_id)
        if not dataBatchById:
            return 404
        
        dataBatchByCode = batch_db.get_batch_by_code(db=db, code=batch.batch_code)
        if dataBatchByCode and dataBatchByCode.batch_id != batch_id:
            return 409
        
        return batch_db.update_batch_by_id(db=db, batch_id=batch_id, batch=batch)
    def delete_batch(self, db: Session, batch_id=int):
        dataBatchById = batch_db.get_batch_by_id(db=db, batch_id=batch_id)
        if not dataBatchById:
            return 404
        
        sub_parameter_employee_db.delete_sub_parameter_employees_by_code(db=db, sub_parameter_employee_code=dataBatchById.batch_code)
        return batch_db.delete_batch_by_id(db=db, batch_id=batch_id)