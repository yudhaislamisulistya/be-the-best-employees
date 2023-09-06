from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.controllers.parameter import ParameterController
from app.config.database import SessionLocal, engine
import app.models.parameter as model_parameter
import app.schemas.parameter as schema_parameter


router = APIRouter(
    prefix="/parameters",
    tags=["parameters"],
    responses={204: {"description": "Not found"}},
)

model_parameter.Base.metadata.create_all(bind=engine)
parameter_controller = ParameterController()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
async def read_parameters(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 1000,
    response: Response = None,
):
    results = parameter_controller.get_parameters(db=db, skip=skip, limit=limit)
    if not results:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"detail": "parameters not found", "status_code": status.HTTP_204_NO_CONTENT}
    
    # loop results and get total weight
    total_weight = 0
    for parameter in results:
        total_weight += parameter.weight
        
    
    response_content = {
        "data": [parameter.as_dict_parameter() for parameter in results],
        "detail": {
            "message": "Successfully get parameters",
            "status_code": status.HTTP_200_OK,
            "total_weight": total_weight,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.get("/relation_sub_parameters")
async def read_parameters_relation_sub_parameters(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 1000,
    response: Response = None,
):
    results = parameter_controller.get_parameters_relation_sub_parameters(db=db, skip=skip, limit=limit)
    if not results:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"detail": "parameters not found", "status_code": status.HTTP_204_NO_CONTENT}
    
    response_content = {
        "data": results,
        "detail": {
            "message": "Successfully get parameters",
            "status_code": status.HTTP_200_OK,
        },
    }
    
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)



@router.post("/")
async def create_parameter(
    parameter: schema_parameter.Parameter, 
    db: Session = Depends(get_db)
):
    results = parameter_controller.create_parameter(db=db, parameter=parameter)
    if not results:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "Parameter already exists",
                "status_code": status.HTTP_409_CONFLICT,
            },
        )
    response_content = {
        "data": results.as_dict_default_parameter(),
        "detail": {
            "message": "Successfully added parameter",
            "status_code": status.HTTP_201_CREATED,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_201_CREATED)

@router.put("/{parameter_id}")
async def update_parameter(
    parameter_id: int,
    parameter: schema_parameter.Parameter,
    db: Session = Depends(get_db)
):
    results = parameter_controller.update_parameter(db=db, parameter_id=parameter_id, parameter=parameter)
    if results == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Parameter not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        )
    
    if results == 409:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "Parameter already exists",
                "status_code": status.HTTP_409_CONFLICT,
            },
        )    
    
    response_content = {
        "data": results.as_dict_default_parameter(),
        "detail": {
            "message": "Successfully updated parameter",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.delete("/{parameter_id}")
async def delete_parameter(
    parameter_id: int,
    db: Session = Depends(get_db)
):
    results = parameter_controller.delete_parameter(db=db, parameter_id=parameter_id)
    if results == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Parameter not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        )
    
    response_content = {
        "data": results.as_dict_default_parameter(),
        "detail": {
            "message": "Successfully deleted parameter",
            "status_code": status.HTTP_200_OK,
        },
    }
    
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)
