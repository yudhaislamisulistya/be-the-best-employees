from sqlalchemy.orm import Session
from fastapi import Request
import app.libs.database.sub_parameter_employee as sub_parameter_employee_db
import app.libs.database.parameter as parameter_db
import app.libs.database.sub_parameter as sub_parameter_db
import app.schemas.sub_parameter_employee as schema_sub_parameter_employee
from collections import defaultdict, OrderedDict
from natsort import natsorted


class SubParameterEmployeeController:
    def get_sub_parameter_employees(self, db: Session, skip: int = 0, limit: int = 1000, sub_parameter_employee_code: str = None, user_id: int = None):
        
        if id and user_id is None:
            sub_parameter_employees = sub_parameter_employee_db.get_sub_parameter_employees(db=db, skip=skip, limit=limit)
        else:
            sub_parameter_employees = sub_parameter_employee_db.get_sub_parameter_employee_by_code_and_user_id(db=db, skip=skip, limit=limit, sub_parameter_employee_code=sub_parameter_employee_code, user_id=user_id)
        return sub_parameter_employees or []
    
    def get_sub_parameter_employees_reference_results(self, db: Session, skip: int = 0, limit: int = 1000, sub_parameter_employee_code: str = None, user_id: int = None):
        
        # if id and user_id is None:
        #     return 404
        # else:
        #     sub_parameter_employees = sub_parameter_employee_db.get_sub_parameter_employee_by_code_and_user_id(db=db, skip=skip, limit=limit, sub_parameter_employee_code=sub_parameter_employee_code, user_id=user_id)
        #     parameters_relation_sub_parameter = parameter_db.get_parameters_relation_sub_parameters(db=db, skip=skip, limit=limit)
        #     parameters = parameter_db.get_parameters(db=db, skip=skip, limit=limit)
        #     sub_parameters = sub_parameter_db.get_sub_parameters(db=db, skip=skip, limit=limit)
        #     uniqueEmployeeCode = []
        #     for sub_parameter_employee in sub_parameter_employees:
        #         if sub_parameter_employee.employee_code not in uniqueEmployeeCode:
        #             uniqueEmployeeCode.append(sub_parameter_employee.employee_code)
                    
        #     total_weight_parameter = 0
        #     for parameter in parameters:
        #         total_weight_parameter += parameter.weight
                
        #     total_weight_sub_parameter = 0
        #     for sub_parameter in sub_parameters:
        #         total_weight_sub_parameter += sub_parameter.weight
                
        #     results = []
        #     for row in parameters_relation_sub_parameter:
        #         for emp_code_a in uniqueEmployeeCode:
        #             for emp_code_b in uniqueEmployeeCode:
        #                 if emp_code_a != emp_code_b:
        #                     result_dict = {
        #                         "parameter_id": row[0],
        #                         "parameter_code": row[1],
        #                         "parameter_name": row[2],
        #                         "parameter_weight": row[3],
        #                         "sub_parameter_id": row[4],
        #                         "sub_parameter_code": row[5],
        #                         "sub_parameter_name": row[6],
        #                         "sub_parameter_weight": row[7],
        #                         "sub_parameter_preference_type": row[8],
        #                         "sub_parameter_target": row[9],
        #                         "sub_parameter_q": row[10],
        #                         "sub_parameter_p": row[11],
        #                         "parameter_result_float": row[3] / total_weight_parameter,
        #                         "parameter_result_string": "{:.3f}".format(row[3] / total_weight_parameter),
        #                         "sub_parameter_result_float": row[7] / total_weight_sub_parameter,
        #                         "sub_parameter_result_string": "{:.3f}".format(row[7] / total_weight_sub_parameter),
        #                         "result_weight_absolute_float": (row[3] / total_weight_parameter) * (row[7] / total_weight_sub_parameter),
        #                         "result_weight_absolute_string": "{:.3f}".format((row[3] / total_weight_parameter) * (row[7] / total_weight_sub_parameter)),
        #                         "total_weight_parameter": total_weight_parameter,
        #                         "total_weight_sub_parameter": total_weight_sub_parameter,
        #                         "employee_code_a": emp_code_a,
        #                         "employee_code_b": emp_code_b,
        #                     }
        #                     results.append(result_dict)
        
        # for result in results:
        #     result["preference_value"] = None
            
        #     for sub_parameter_employee in sub_parameter_employees:
        #         if result["sub_parameter_code"] == sub_parameter_employee.sub_parameter_code and result["employee_code_a"] == sub_parameter_employee.employee_code:
        #             result["value_a"] = sub_parameter_employee.value
        #         if result["sub_parameter_code"] == sub_parameter_employee.sub_parameter_code and result["employee_code_b"] == sub_parameter_employee.employee_code:
        #             result["value_b"] = sub_parameter_employee.value
                    
        #     result["value_d"] = result["value_a"] - result["value_b"]
            
        #     if result["sub_parameter_preference_type"] == "Tipe I":
        #         result["preference_value"] = 0
        #         result["preference_index_value"] = 0
                
        #     if result["sub_parameter_preference_type"] == "Tipe II":
        #         result["preference_value"] = 0
        #         result["preference_index_value"] = 0
            
        #     if result["sub_parameter_preference_type"] == "Tipe III":
        #         if result["value_d"] < 5:
        #             result["preference_value"] = 0
        #         elif result["value_d"] >= 5 and result["value_d"] < 10:
        #             result["preference_value"] = round(result["value_d"] / result["sub_parameter_p"], 3)
        #         else:
        #             result["preference_value"] = 0
                
        #         if result["preference_value"] is not None:
        #             result["preference_index_value"] = round(result["preference_value"] * result["result_weight_absolute_float"], 3)
            
        #     if result["sub_parameter_preference_type"] == "Tipe IV":
        #         result["preference_value"] = 0
        #         result["preference_index_value"] = 0
                
        #     if result["sub_parameter_preference_type"] == "Tipe V":
        #         result["preference_value"] = 0
        #         result["preference_index_value"] = 0
                
        #     if result["sub_parameter_preference_type"] == "Tipe VI":
        #         result["preference_value"] = 0
        #         result["preference_index_value"] = 0
        
        # return results or []
        if id is None or user_id is None:
            return 404
        
        sub_parameter_employees = sub_parameter_employee_db.get_sub_parameter_employee_by_code_and_user_id(db=db, skip=skip, limit=limit, sub_parameter_employee_code=sub_parameter_employee_code, user_id=user_id)
        parameters_relation_sub_parameter = parameter_db.get_parameters_relation_sub_parameters(db=db, skip=skip, limit=limit)
        parameters = parameter_db.get_parameters(db=db, skip=skip, limit=limit)
        sub_parameters = sub_parameter_db.get_sub_parameters(db=db, skip=skip, limit=limit)
        
        uniqueEmployeeCode = list(set(sub_parameter_employee.employee_code for sub_parameter_employee in sub_parameter_employees))
        
        results = get_results(sub_parameter_employees, parameters_relation_sub_parameter, parameters, sub_parameters, uniqueEmployeeCode)
        # sort by employee_code_a and employee_code_b, sub_parameter_code
        results = natsorted(results, key=lambda k: (k['employee_code_a'], k['employee_code_b'], k['sub_parameter_code']))
        
        
        result_preference_index_promethee = defaultdict(lambda: defaultdict(int))
        result_preference_index_promethee_string = defaultdict(lambda: defaultdict(str))
        for result in results:
            result_preference_index_promethee[result["employee_code_a"]][result["employee_code_b"]] += round(result["preference_index_value"], 3)
            result_preference_index_promethee_string[result["employee_code_a"]][result['employee_code_b']] = "{:.3f}".format(result_preference_index_promethee[result["employee_code_a"]][result["employee_code_b"]])
            result_preference_index_promethee[result["employee_code_a"]][result["employee_code_b"]] = round(result_preference_index_promethee[result["employee_code_a"]][result["employee_code_b"]], 3)
        
        for employee_code in result_preference_index_promethee_string:
            result_preference_index_promethee_string[employee_code][employee_code] = "0.000"
            result_preference_index_promethee[employee_code][employee_code] = 0.0
        
        sorted_preference_index_promethee_string = OrderedDict()
        for employee_code, inner_dict in result_preference_index_promethee_string.items():
            sorted_preference_index_promethee_string[employee_code] = OrderedDict(natsorted(inner_dict.items()))
            
        sorted_preference_index_promethee = OrderedDict()
        for employee_code, inner_dict in result_preference_index_promethee.items():
            sorted_preference_index_promethee[employee_code] = OrderedDict(natsorted(inner_dict.items()))
            
        # leaving flow menjumlalah perbaris employee_code_a
        sorted_leaving_flow = OrderedDict()
        sorted_leaving_flow_string = OrderedDict()
        for employee_code_a in sorted_preference_index_promethee:
            sorted_leaving_flow[employee_code_a] = round(sum(sorted_preference_index_promethee[employee_code_a].values())/9, 3)
            sorted_leaving_flow_string[employee_code_a] = "{:.3f}".format(sorted_leaving_flow[employee_code_a])
            
        # entering flow menjumlahkan perkolom employee_code_b
        # entering flow menjumlahkan perkolom employee_code_b
        columns_preference_index_promethee = defaultdict(lambda: defaultdict(int))
        for employee_code_a in sorted_preference_index_promethee:
            for employee_code_b in sorted_preference_index_promethee[employee_code_a]:
                columns_preference_index_promethee[employee_code_b][employee_code_a] = sorted_preference_index_promethee[employee_code_a][employee_code_b]
        
        sorted_entering_flow = OrderedDict()
        sorted_entering_flow_string = OrderedDict()
        for employee_code_b in columns_preference_index_promethee:
            sorted_entering_flow[employee_code_b] = round(sum(columns_preference_index_promethee[employee_code_b].values())/9, 3)
            sorted_entering_flow_string[employee_code_b] = "{:.3f}".format(sorted_entering_flow[employee_code_b])
            
        sorted_net_flow = OrderedDict()
        sorted_net_flow_string = OrderedDict()
        for employee_code in sorted_leaving_flow:
            sorted_net_flow[employee_code] = round(sorted_leaving_flow[employee_code] - sorted_entering_flow[employee_code], 3)
            sorted_net_flow_string[employee_code] = "{:.3f}".format(sorted_net_flow[employee_code])
            
        ranking_by_sorted_net_flow = natsorted(sorted_net_flow.items(), key=lambda k: k[1], reverse=True)
        ranking_by_sorted_net_flow = [(i+1, employee_code, net_flow) for i, (employee_code, net_flow) in enumerate(ranking_by_sorted_net_flow)]
        
        final_results = {
            "data": results,
            "preference_index_promethee": sorted_preference_index_promethee,
            "preference_index_promethee_string": sorted_preference_index_promethee_string,
            "leaving_flow": sorted_leaving_flow,
            "leaving_flow_string": sorted_leaving_flow_string,
            "columns_preference_index_promethee": columns_preference_index_promethee,
            "entering_flow": sorted_entering_flow,
            "entering_flow_string": sorted_entering_flow_string,
            "net_flow": sorted_net_flow,
            "net_flow_string": sorted_net_flow_string,
            "ranking": ranking_by_sorted_net_flow,
        }
        
        
        
        return final_results or []
    
    def create_sub_parameter_employee(self, db: Session, sub_parameter_employee=schema_sub_parameter_employee.SubParameterEmployee):
        return sub_parameter_employee_db.create_sub_parameter_employee(db=db, sub_parameter_employee=sub_parameter_employee)
    
    def bulk_create_sub_parameter_employee(self, db: Session, data: Request):
        sub_parameter_employee_db.bulk_create_sub_parameter_employee(db=db, sub_parameter_employees=data)
        return 201
    
    def bulk_update_sub_parameter_employee(self, db: Session, data: Request):
        print(data)
        sub_parameter_employee_db.bulk_update_sub_parameter_employee(db=db, sub_parameter_employees=data)
        return 201
    
    def update_sub_parameter_employee(self, db: Session, sub_parameter_employee_id=int, sub_parameter_employee=schema_sub_parameter_employee.SubParameterEmployee):
        GradedataSubParameterById = sub_parameter_employee_db.get_sub_parameter_employee_by_id(db=db, sub_parameter_employee_id=sub_parameter_employee_id)
        if not GradedataSubParameterById:
            return 404
        
        return sub_parameter_employee_db.update_sub_parameter_employee_by_id(db=db, sub_parameter_employee_id=sub_parameter_employee_id, sub_parameter_employee=sub_parameter_employee)
    
    def delete_sub_parameter_employee(db: Session, sub_parameter_employee_id=int):
        GradedataSubParameterById = sub_parameter_employee_db.get_sub_parameter_employee_by_id(db=db, sub_parameter_employee_id=sub_parameter_employee_id)
        if not GradedataSubParameterById:
            return 404
        
        return sub_parameter_employee_db.delete_sub_parameter_employee_by_id(db=db, sub_parameter_employee_id=sub_parameter_employee_id)
    
def optimize_sub_parameter_employees(sub_parameter_employees, uniqueEmployeeCode):
    employee_values = defaultdict(lambda: defaultdict(int))
    
    for sub_parameter_employee in sub_parameter_employees:
        employee_values[sub_parameter_employee.sub_parameter_code][sub_parameter_employee.employee_code] = sub_parameter_employee.value
    
    return employee_values

def calculate_preference_value_tipe_III(value_d, sub_parameter_p):
    if value_d < 5:
        return 0
    elif 5 <= value_d < 10:
        return round(value_d / sub_parameter_p, 3)
    else:
        return 0
    
def calculate_preference_value_tipe_IV(value_d, sub_parameter_q, sub_parameter_p):
    if value_d <= sub_parameter_q:
        return 0
    elif sub_parameter_q < value_d <= sub_parameter_p:
        return 1/2
    elif value_d > sub_parameter_p:
        return  1

def calculate_preference_value_tipe_I(value_d):
    if value_d <= 0:
        return 0
    elif value_d > 0:
        return 1

def calculate_preference_index_value(preference_value, result_weight_absolute_float):
    if preference_value is not None:
        return round(preference_value * result_weight_absolute_float, 3)
    return 0

def get_results(sub_parameter_employees, parameters_relation_sub_parameter, parameters, sub_parameters, uniqueEmployeeCode):
    total_weight_parameter = sum(parameter.weight for parameter in parameters)
    total_weight_sub_parameter = sum(sub_parameter.weight for sub_parameter in sub_parameters)
    
    employee_values = optimize_sub_parameter_employees(sub_parameter_employees, uniqueEmployeeCode)
    
    results = []
    for row in parameters_relation_sub_parameter:
        for emp_code_a in uniqueEmployeeCode:
            for emp_code_b in uniqueEmployeeCode:
                if emp_code_a != emp_code_b:
                    value_a = employee_values.get(row[5], {}).get(emp_code_a, 0)
                    value_b = employee_values.get(row[5], {}).get(emp_code_b, 0)
                    value_d = value_a - value_b
                    
                    preference_value = None
                    if row[8] == "Tipe III":
                        preference_value = calculate_preference_value_tipe_III(value_d, row[11])
                    elif row[8] == "Tipe IV":
                        preference_value = calculate_preference_value_tipe_IV(value_d, row[10], row[11])
                    elif row[8] == "Tipe I":
                        preference_value = calculate_preference_value_tipe_I(value_d)
                    
                    preference_index_value = calculate_preference_index_value(preference_value, (row[3] / total_weight_parameter) * (row[7] / total_weight_sub_parameter))
                    
                    result_dict = {
                        "parameter_id": row[0],
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
                        "total_weight_sub_parameter": total_weight_sub_parameter,
                        "employee_code_a": emp_code_a,
                        "employee_code_b": emp_code_b,
                        "preference_value": preference_value,
                        "preference_index_value": preference_index_value,
                        "value_a": value_a,
                        "value_b": value_b,
                        "value_d": value_d,
                    }
                    results.append(result_dict)
    
    return results