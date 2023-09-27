from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.controllers.sub_parameter import SubParameterController
from app.config.database import SessionLocal, engine
import app.models.sub_parameter as model_sub_parameter
import app.schemas.sub_parameter as schema_sub_parameter


router = APIRouter(
    prefix="/sub_parameters",
    tags=["sub_parameters"],
    responses={204: {"description": "Not found"}},
)

model_sub_parameter.Base.metadata.create_all(bind=engine)
sub_parameter_controller = SubParameterController()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
async def read_sub_parameters(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 1000,
    response: Response = None,
):
    results = sub_parameter_controller.get_sub_parameters(db=db, skip=skip, limit=limit)
    if not results:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"detail": "sub_parameters not found", "status_code": status.HTTP_204_NO_CONTENT}
    
    total_weight = 0
    for sub_parameter in results:
        total_weight += sub_parameter.weight
    
    response_content = {
        "data": [sub_parameter.as_dict_sub_parameter() for sub_parameter in results],
        "detail": {
            "message": "Successfully get sub_parameters",
            "status_code": status.HTTP_200_OK,
            "total_weight": total_weight,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)


@router.post("/")
async def create_sub_parameter(
    sub_parameter: schema_sub_parameter.SubParameter, 
    db: Session = Depends(get_db)
):
    results = sub_parameter_controller.create_sub_parameter(db=db, sub_parameter=sub_parameter)
    if not results:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "SubParameter already exists",
                "status_code": status.HTTP_409_CONFLICT,
            },
        )
    response_content = {
        "data": results.as_dict_default_sub_parameter(),
        "detail": {
            "message": "Successfully added sub_parameter",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.put("/{sub_parameter_id}")
async def update_sub_parameter(
    sub_parameter_id: int,
    sub_parameter: schema_sub_parameter.SubParameter,
    db: Session = Depends(get_db)
):
    results = sub_parameter_controller.update_sub_parameter(db=db, sub_parameter_id=sub_parameter_id, sub_parameter=sub_parameter)
    if results == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "SubParameter not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        )
    
    if results == 409:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "SubParameter already exists",
                "status_code": status.HTTP_409_CONFLICT,
            },
        )    
    
    response_content = {
        "data": results.as_dict_default_sub_parameter(),
        "detail": {
            "message": "Successfully updated sub_parameter",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.delete("/{sub_parameter_id}")
async def delete_sub_parameter(
    sub_parameter_id: int,
    db: Session = Depends(get_db)
):
    results = sub_parameter_controller.delete_sub_parameter(db=db, sub_parameter_id=sub_parameter_id)
    if results == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "SubParameter not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        )
    
    response_content = {
        "data": results.as_dict_default_sub_parameter(),
        "detail": {
            "message": "Successfully deleted sub_parameter",
            "status_code": status.HTTP_200_OK,
        },
    }
    
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)
