from fastapi import APIRouter
from app.endpoints import ranking

router = APIRouter()
router.include_router(ranking.router)