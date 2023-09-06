from fastapi import APIRouter
from app.endpoints import parameter

router = APIRouter()
router.include_router(parameter.router)