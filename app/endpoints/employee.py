from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.controllers.employee import EmployeeController
from app.config.database import SessionLocal, engine
import app.models.employee as model_employee
import app.schemas.employee as schema_employee


router = APIRouter(
    prefix="/employees",
    tags=["employees"],
)

model_employee.Base.metadata.create_all(bind=engine)
employee_controller = EmployeeController()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
async def read_employees(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 1000,
    response: Response = None,
):
    results = employee_controller.get_employees(db=db, skip=skip, limit=limit)
    if not results:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"detail": "employees not found", "status_code": status.HTTP_204_NO_CONTENT}
    
    response_content = {
        "data": [employee.as_dict_employee() for employee in results],
        "detail": {
            "message": "Successfully get employees",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)


@router.post("/")
async def create_employee(
    employee: schema_employee.Employee, 
    db: Session = Depends(get_db)
):
    results = employee_controller.create_employee(db=db, employee=employee)
    if not results:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "Employee already exists",
                "status_code": status.HTTP_409_CONFLICT,
            },
        )
    response_content = {
        "data": results.as_dict_employee(),
        "detail": {
            "message": "Successfully added employee",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.put("/{employee_id}")
async def update_employee(
    employee_id: int,
    employee: schema_employee.Employee,
    db: Session = Depends(get_db)
):
    results = employee_controller.update_employee(db=db, employee_id=employee_id, employee=employee)
    if results == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Employee not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        )
    
    if results == 409:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "Employee already exists",
                "status_code": status.HTTP_409_CONFLICT,
            },
        )    
    
    response_content = {
        "data": results.as_dict_employee(),
        "detail": {
            "message": "Successfully updated employee",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    results = employee_controller.delete_employee(db=db, employee_id=employee_id)
    if results == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Employee not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        )
    
    response_content = {
        "data": results.as_dict_employee(),
        "detail": {
            "message": "Successfully deleted employee",
            "status_code": status.HTTP_200_OK,
        },
    }
    
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)
