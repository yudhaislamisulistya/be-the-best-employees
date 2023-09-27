from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.controllers.batch import BatchController
from app.config.database import SessionLocal, engine
import app.models.batch as model_batch
import app.schemas.batch as schema_batch


router = APIRouter(
    prefix="/batchs",
    tags=["batchs"],
)

model_batch.Base.metadata.create_all(bind=engine)
batch_controller = BatchController()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
async def read_batchs(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 1000,
    response: Response = None,
):
    results = batch_controller.get_batchs(db=db, skip=skip, limit=limit)
    if not results:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"detail": "batchs not found", "status_code": status.HTTP_204_NO_CONTENT}
    
    response_content = {
        "data": [batch.as_dict_batch() for batch in results],
        "detail": {
            "message": "Successfully get batchs",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)


@router.post("/")
async def create_batch(
    batch: schema_batch.Batch, 
    db: Session = Depends(get_db)
):
    results = batch_controller.create_batch(db=db, batch=batch)
    if not results:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "Batch already exists",
                "status_code": status.HTTP_409_CONFLICT,
            },
        )
    response_content = {
        "data": results.as_dict_batch(),
        "detail": {
            "message": "Successfully added batch",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.put("/{batch_id}")
async def update_batch(
    batch_id: int,
    batch: schema_batch.Batch,
    db: Session = Depends(get_db)
):
    results = batch_controller.update_batch(db=db, batch_id=batch_id, batch=batch)
    if results == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Batch not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        )
    
    if results == 409:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "Batch already exists",
                "status_code": status.HTTP_409_CONFLICT,
            },
        )    
    
    response_content = {
        "data": results.as_dict_batch(),
        "detail": {
            "message": "Successfully updated batch",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.delete("/{batch_id}")
async def delete_batch(
    batch_id: int,
    db: Session = Depends(get_db)
):
    results = batch_controller.delete_batch(db=db, batch_id=batch_id)
    if results == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Batch not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        )
    
    response_content = {
        "data": results.as_dict_batch(),
        "detail": {
            "message": "Successfully deleted batch",
            "status_code": status.HTTP_200_OK,
        },
    }
    
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)
