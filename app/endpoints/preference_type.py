from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.controllers.preference_type import PreferenceTypeController
from app.config.database import SessionLocal, engine
import app.models.preference_type as model_preference_type
import app.schemas.preference_type as schema_preference_type


router = APIRouter(
    prefix="/preference_types",
    tags=["preference_types"],
    responses={204: {"description": "Not found"}},
)

model_preference_type.Base.metadata.create_all(bind=engine)
preference_type_controller = PreferenceTypeController()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
async def read_preference_types(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 1000,
    response: Response = None,
):
    results = preference_type_controller.get_preference_types(db=db, skip=skip, limit=limit)
    if not results:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"detail": "preference_types not found", "status_code": status.HTTP_204_NO_CONTENT}
    
    
    response_content = {
        "data": [preference_type.as_dict_default_preference_type() for preference_type in results],
        "detail": {
            "message": "Successfully get preference_types",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.post("/")
async def create_preference_type(
    preference_type: schema_preference_type.PreferenceType, 
    db: Session = Depends(get_db)
):
    results = preference_type_controller.create_preference_type(db=db, preference_type=preference_type)
    if not results:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "PreferenceType already exists",
                "status_code": status.HTTP_409_CONFLICT,
            },
        )
    response_content = {
        "data": results.as_dict_default_preference_type(),
        "detail": {
            "message": "Successfully added preference_type",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.put("/{preference_type_id}")
async def update_preference_type(
    preference_type_id: int,
    preference_type: schema_preference_type.PreferenceType,
    db: Session = Depends(get_db)
):
    results = preference_type_controller.update_preference_type(db=db, preference_type_id=preference_type_id, preference_type=preference_type)
    if results == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "PreferenceType not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        )
    
    if results == 409:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "PreferenceType already exists",
                "status_code": status.HTTP_409_CONFLICT,
            },
        )    
    
    response_content = {
        "data": results.as_dict_default_preference_type(),
        "detail": {
            "message": "Successfully updated preference_type",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.delete("/{preference_type_id}")
async def delete_preference_type(
    preference_type_id: int,
    db: Session = Depends(get_db)
):
    results = preference_type_controller.delete_preference_type(db=db, preference_type_id=preference_type_id)
    if results == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "PreferenceType not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        )
    
    response_content = {
        "data": results.as_dict_default_preference_type(),
        "detail": {
            "message": "Successfully deleted preference_type",
            "status_code": status.HTTP_200_OK,
        },
    }
    
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)
