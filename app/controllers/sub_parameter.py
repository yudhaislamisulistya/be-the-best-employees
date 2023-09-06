from sqlalchemy.orm import Session
import app.libs.database.sub_parameter as sub_parameter_db
import app.schemas.sub_parameter as schema_sub_parameter

class SubParameterController:
    def get_sub_parameters(self, db: Session, skip: int = 0, limit: int = 1000):
        sub_parameters = sub_parameter_db.get_sub_parameters(db=db, skip=skip, limit=limit)
        
        total_weight = 0
        for sub_parameter in sub_parameters:
            total_weight += sub_parameter.weight
            
        for sub_parameter in sub_parameters:
            sub_parameter.result_float = sub_parameter.weight / total_weight
            sub_parameter.result_string = "{:.3f}".format(sub_parameter.result_float)
        
        return sub_parameters or []
    def create_sub_parameter(self, db: Session, sub_parameter=schema_sub_parameter.SubParameter):
        data = sub_parameter_db.get_sub_parameter_by_code(db=db, code=sub_parameter.sub_parameter_code)
        if data:
            return False
        
        return sub_parameter_db.create_sub_parameter(db=db, sub_parameter=sub_parameter)
    def update_sub_parameter(self, db: Session, sub_parameter_id=int, sub_parameter=schema_sub_parameter.SubParameter):
        dataSubParameterById = sub_parameter_db.get_sub_parameter_by_id(db=db, sub_parameter_id=sub_parameter_id)
        if not dataSubParameterById:
            return 404
        
        dataSubParameterByCode = sub_parameter_db.get_sub_parameter_by_code(db=db, code=sub_parameter.sub_parameter_code)
        if dataSubParameterByCode and dataSubParameterByCode.sub_parameter_id != sub_parameter_id:
            return 409
        
        return sub_parameter_db.update_sub_parameter_by_id(db=db, sub_parameter_id=sub_parameter_id, sub_parameter=sub_parameter)
    def delete_sub_parameter(self, db: Session, sub_parameter_id=int):
        dataSubParameterById = sub_parameter_db.get_sub_parameter_by_id(db=db, sub_parameter_id=sub_parameter_id)
        if not dataSubParameterById:
            return 404
        
        return sub_parameter_db.delete_sub_parameter_by_id(db=db, sub_parameter_id=sub_parameter_id)