from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.controllers.grade_sub_parameter import GradeSubParameterController
from app.config.database import SessionLocal, engine
import app.models.grade_sub_parameter as grade_model_sub_parameter
import app.schemas.grade_sub_parameter as grade_schema_sub_parameter


router = APIRouter(
    prefix="/grade_sub_parameters",
    tags=["grade_sub_parameters"],
    responses={204: {"description": "Not found"}},
)

grade_model_sub_parameter.Base.metadata.create_all(bind=engine)
grade_sub_parameter_controller = GradeSubParameterController()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
async def get_grade_sub_parameters(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 1000,
    response: Response = None,
):
    results = grade_sub_parameter_controller.get_grade_sub_parameters(db=db, skip=skip, limit=limit)
    if not results:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"detail": "grade_sub_parameters not found", "status_code": status.HTTP_204_NO_CONTENT}
    
    response_content = {
        "data": [grade_sub_parameter.as_dict_grade_sub_parameter() for grade_sub_parameter in results],
        "detail": {
            "message": "Successfully get grade_sub_parameters",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)


@router.post("/")
async def create_grade_sub_parameter(
    grade_sub_parameter: grade_schema_sub_parameter.GradeSubParameter, 
    db: Session = Depends(get_db)
):
    results = grade_sub_parameter_controller.create_grade_sub_parameter(db=db, grade_sub_parameter=grade_sub_parameter)
    if not results:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "GradeSubParameter already exists",
                "status_code": status.HTTP_409_CONFLICT,
            },
        )
    response_content = {
        "data": results.as_dict_grade_sub_parameter(),
        "detail": {
            "message": "Successfully added grade_sub_parameter",
            "status_code": status.HTTP_201_CREATED,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_201_CREATED)

@router.put("/{grade_sub_parameter_id}")
async def update_grade_sub_parameter(
    grade_sub_parameter_id: int,
    grade_sub_parameter: grade_schema_sub_parameter.GradeSubParameter,
    db: Session = Depends(get_db)
):
    results = grade_sub_parameter_controller.update_grade_sub_parameter(db=db, grade_sub_parameter_id=grade_sub_parameter_id, grade_sub_parameter=grade_sub_parameter)
    if results == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "GradeSubParameter not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        )
    
    if results == 409:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "GradeSubParameter already exists",
                "status_code": status.HTTP_409_CONFLICT,
            },
        )    
    
    response_content = {
        "data": results.as_dict_grade_sub_parameter(),
        "detail": {
            "message": "Successfully updated grade_sub_parameter",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.delete("/{grade_sub_parameter_id}")
async def delete_grade_sub_parameter(
    grade_sub_parameter_id: int,
    db: Session = Depends(get_db)
):
    results = grade_sub_parameter_controller.delete_grade_sub_parameter(db=db, grade_sub_parameter_id=grade_sub_parameter_id)
    if results == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "GradeSubParameter not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        )
    
    response_content = {
        "data": results.as_dict_grade_sub_parameter(),
        "detail": {
            "message": "Successfully deleted grade_sub_parameter",
            "status_code": status.HTTP_200_OK,
        },
    }
    
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)
