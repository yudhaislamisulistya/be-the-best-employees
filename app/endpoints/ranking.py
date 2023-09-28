from fastapi import APIRouter, Depends, Response, status, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.controllers.ranking import RankingController
from app.config.database import SessionLocal, engine
import app.models.ranking as model_ranking
import app.schemas.ranking as schema_ranking


router = APIRouter(
    prefix="/rankings",
    tags=["rankings"],
    responses={204: {"description": "Not found"}},
)

model_ranking.Base.metadata.create_all(bind=engine)
ranking_controller = RankingController()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
async def read_rankings(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 1000,
    response: Response = None,
):
    results = ranking_controller.get_rankings(db=db, skip=skip, limit=limit)
    if not results:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"detail": "rankings not found", "status_code": status.HTTP_204_NO_CONTENT}
    
    
    response_content = {
        "data": [ranking.as_dict_default_ranking() for ranking in results],
        "detail": {
            "message": "Successfully get rankings",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.get("/copeland")
async def read_rankings_copeland(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 1000,
    response: Response = None,
):
    results = ranking_controller.get_rankings_copeland(db=db, skip=skip, limit=limit)
    return JSONResponse(content=results, status_code=status.HTTP_200_OK)

@router.post("/")
async def create_ranking(
    ranking: schema_ranking.Ranking, 
    db: Session = Depends(get_db)
):
    results = ranking_controller.create_ranking(db=db, ranking=ranking)
    if not results:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "Ranking already exists",
                "status_code": status.HTTP_409_CONFLICT,
            },
        )
    response_content = {
        "data": results.as_dict_default_ranking(),
        "detail": {
            "message": "Successfully added ranking",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.post("/bulk")
async def bulk_create_or_update_ranking(
    request: Request,
    db: Session = Depends(get_db)
):
    rankings = await request.json()
    top_ranking = rankings[0]
    top_rangking_by_batch_code_and_user_id = ranking_controller.get_ranking_by_batch_code_and_user_id(db=db, batch_code=top_ranking["batch_code"], user_id=top_ranking["user_id"])
    
    if top_rangking_by_batch_code_and_user_id == 404:
        results = ranking_controller.bulk_create_ranking(db=db, data=rankings)
    else:
        results = ranking_controller.bulk_create_or_update_ranking(db=db, data=rankings)
    
    response_content = {
        "data": results,
        "detail": {
            "message": "Successfully added rankings",
            "status_code": status.HTTP_201_CREATED,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.put("/{ranking_id}")
async def update_ranking(
    ranking_id: int,
    ranking: schema_ranking.Ranking,
    db: Session = Depends(get_db)
):
    results = ranking_controller.update_ranking(db=db, ranking_id=ranking_id, ranking=ranking)
    if results == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Ranking not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        )
    
    if results == 409:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "Ranking already exists",
                "status_code": status.HTTP_409_CONFLICT,
            },
        )    
    
    response_content = {
        "data": results.as_dict_default_ranking(),
        "detail": {
            "message": "Successfully updated ranking",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.delete("/{ranking_id}")
async def delete_ranking(
    ranking_id: int,
    db: Session = Depends(get_db)
):
    results = ranking_controller.delete_ranking(db=db, ranking_id=ranking_id)
    if results == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Ranking not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        )
    
    response_content = {
        "data": results.as_dict_default_ranking(),
        "detail": {
            "message": "Successfully deleted ranking",
            "status_code": status.HTTP_200_OK,
        },
    }
    
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)
