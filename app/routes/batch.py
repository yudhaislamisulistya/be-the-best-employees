from fastapi import APIRouter
from app.endpoints import batch

router = APIRouter()
router.include_router(batch.router)