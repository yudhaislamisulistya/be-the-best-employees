from sqlalchemy.orm import Session
import app.libs.database.parameter as parameter_db
import app.libs.database.sub_parameter as sub_parameter_db
import app.schemas.parameter as schema_parameter

class ParameterController:
    def get_parameters(self, db: Session, skip: int = 0, limit: int = 1000):
        parameters = parameter_db.get_parameters(db=db, skip=skip, limit=limit)
        
        total_weight = 0
        for parameter in parameters:
            total_weight += parameter.weight
            
        for parameter in parameters:
            parameter.result_float = parameter.weight / total_weight
            parameter.result_string = "{:.3f}".format(parameter.result_float)
        
        return parameters or []
    
    def get_parameters_relation_sub_parameters(self, db: Session, skip: int = 0, limit: int = 1000):
        parameters_relation_sub_parameter = parameter_db.get_parameters_relation_sub_parameters(db=db, skip=skip, limit=limit)
        parameters = parameter_db.get_parameters(db=db, skip=skip, limit=limit)
        sub_parameters = sub_parameter_db.get_sub_parameters(db=db, skip=skip, limit=limit)
        
        total_weight_parameter = 0
        for parameter in parameters:
            total_weight_parameter += parameter.weight
            
        total_weight_sub_parameter = 0
        for sub_parameter in sub_parameters:
            total_weight_sub_parameter += sub_parameter.weight
        


        final_results = []
        for row in parameters_relation_sub_parameter:
            result_dict = {
                "parameter_id": row[0],
                "parameter_code": row[1],
                "parameter_name": row[2],
                "parameter_weight": row[3],
                "sub_parameter_id": row[4],
                "sub_parameter_code": row[5],
                "sub_parameter_name": row[6],
                "sub_parameter_weight": row[7],
                "sub_parameter_preference_type": row[8],
                "sub_parameter_target": row[9],
                "sub_parameter_q": row[10],
                "sub_parameter_p": row[11],
                "parameter_result_float": row[3] / total_weight_parameter,
                "parameter_result_string": "{:.3f}".format(row[3] / total_weight_parameter),
                "sub_parameter_result_float": row[7] / total_weight_sub_parameter,
                "sub_parameter_result_string": "{:.3f}".format(row[7] / total_weight_sub_parameter),
                "result_weight_absolute_float": (row[3] / total_weight_parameter) * (row[7] / total_weight_sub_parameter),
                "result_weight_absolute_string": "{:.3f}".format((row[3] / total_weight_parameter) * (row[7] / total_weight_sub_parameter)),
                "total_weight_parameter": total_weight_parameter,
                "total_weight_sub_parameter": total_weight_sub_parameter
            }
            final_results.append(result_dict)
        
        return final_results or []
        
    def create_parameter(self, db: Session, parameter=schema_parameter.Parameter):
        data = parameter_db.get_parameter_by_code(db=db, code=parameter.parameter_code)
        if data:
            return False
        
        return parameter_db.create_parameter(db=db, parameter=parameter)
    def update_parameter(self, db: Session, parameter_id=int, parameter=schema_parameter.Parameter):
        dataParameterById = parameter_db.get_parameter_by_id(db=db, parameter_id=parameter_id)
        if not dataParameterById:
            return 404
        
        dataParameterByCode = parameter_db.get_parameter_by_code(db=db, code=parameter.parameter_code)
        if dataParameterByCode and dataParameterByCode.parameter_id != parameter_id:
            return 409
        
        return parameter_db.update_parameter_by_id(db=db, parameter_id=parameter_id, parameter=parameter)
    def delete_parameter(self, db: Session, parameter_id=int):
        dataParameterById = parameter_db.get_parameter_by_id(db=db, parameter_id=parameter_id)
        if not dataParameterById:
            return 404
        
        return parameter_db.delete_parameter_by_id(db=db, parameter_id=parameter_id)