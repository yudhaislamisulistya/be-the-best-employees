from fastapi import APIRouter, Depends, Response, status, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.controllers.sub_parameter_employee import SubParameterEmployeeController
from app.config.database import SessionLocal, engine
import app.models.sub_parameter_employee as model_sub_parameter_employee
import app.schemas.sub_parameter_employee as schema_sub_parameter_employee


router = APIRouter(
    prefix="/sub_parameter_employees",
    tags=["sub_parameter_employees"],
    responses={204: {"description": "Not found"}},
)

model_sub_parameter_employee.Base.metadata.create_all(bind=engine)
sub_parameter_employee_controller = SubParameterEmployeeController()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
async def read_sub_parameter_employees(
    db: Session = Depends(get_db),
    sub_parameter_employee_code: str = None,
    user_id: int = None,
    skip: int = 0,
    limit: int = 1000,
    response: Response = None,
):
    results = sub_parameter_employee_controller.get_sub_parameter_employees(db=db, skip=skip, limit=limit, sub_parameter_employee_code=sub_parameter_employee_code, user_id=user_id)
    if not results:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"detail": "sub_parameter_employees not found", "status_code": status.HTTP_204_NO_CONTENT}
    
    response_content = {
        "data": [sub_parameter_employee.as_dict_default_sub_parameter_employee() for sub_parameter_employee in results],
        "detail": {
            "message": "Successfully get sub_parameter_employees",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.get("/reference_results")
async def read_sub_parameter_employees_reference_results(
    db: Session = Depends(get_db),
    sub_parameter_employee_code: str = None,
    user_id: int = None,
    skip: int = 0,
    limit: int = 1000,
):
    results = sub_parameter_employee_controller.get_sub_parameter_employees_reference_results(db=db, skip=skip, limit=limit, sub_parameter_employee_code=sub_parameter_employee_code, user_id=user_id)

    return JSONResponse(content=results, status_code=status.HTTP_200_OK)

@router.post("/")
async def create_sub_parameter_employee(
    sub_parameter_employee: schema_sub_parameter_employee.SubParameterEmployee, 
    db: Session = Depends(get_db)
):
    results = sub_parameter_employee_controller.create_sub_parameter_employee(db=db, sub_parameter_employee=sub_parameter_employee)
    if not results:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "SubParameterEmployee already exists",
                "status_code": status.HTTP_409_CONFLICT,
            },
        )
    response_content = {
        "data": results.as_dict_default_sub_parameter_employee(),
        "detail": {
            "message": "Successfully added sub_parameter_employee",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.post("/batch")
async def create_sub_parameter_employee_batch(
    request: Request,
    db: Session = Depends(get_db)
):
    data = await request.json()
    results = sub_parameter_employee_controller.bulk_create_sub_parameter_employee(db=db, data=data)

    response_content = {
        "data": results,
        "detail": {
            "message": "Successfully added sub_parameter_employee",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.put("/batch")
async def create_sub_parameter_employee_batch(
    request: Request,
    db: Session = Depends(get_db)
):
    data = await request.json()
    results = sub_parameter_employee_controller.bulk_update_sub_parameter_employee(db=db, data=data)

    response_content = {
        "data": results,
        "detail": {
            "message": "Successfully updated sub_parameter_employee",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.put("/{sub_parameter_employee_id}")
async def update_sub_parameter_employee(
    sub_parameter_employee_id: int,
    sub_parameter_employee: schema_sub_parameter_employee.SubParameterEmployee,
    db: Session = Depends(get_db)
):
    results = sub_parameter_employee_controller.update_sub_parameter_employee(db=db, sub_parameter_employee_id=sub_parameter_employee_id, sub_parameter_employee=sub_parameter_employee)
    if results == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "SubParameterEmployee not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        )
    
    if results == 409:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "SubParameterEmployee already exists",
                "status_code": status.HTTP_409_CONFLICT,
            },
        )    
    
    response_content = {
        "data": results.as_dict_default_sub_parameter_employee(),
        "detail": {
            "message": "Successfully updated sub_parameter_employee",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.delete("/{sub_parameter_employee_id}")
async def delete_sub_parameter_employee(
    sub_parameter_employee_id: int,
    db: Session = Depends(get_db)
):
    results = sub_parameter_employee_controller.delete_sub_parameter_employee(db=db, sub_parameter_employee_id=sub_parameter_employee_id)
    if results == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "SubParameterEmployee not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        )
    
    response_content = {
        "data": results.as_dict_default_sub_parameter_employee(),
        "detail": {
            "message": "Successfully deleted sub_parameter_employee",
            "status_code": status.HTTP_200_OK,
        },
    }
    
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)
