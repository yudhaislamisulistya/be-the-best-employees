from fastapi import APIRouter
from app.endpoints import preference_type

router = APIRouter()
router.include_router(preference_type.router)