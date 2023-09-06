from fastapi import APIRouter
from app.endpoints import user

router = APIRouter()
router.include_router(user.router)