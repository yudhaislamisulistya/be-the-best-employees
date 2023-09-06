from fastapi import APIRouter
from app.endpoints import sub_parameter

router = APIRouter()
router.include_router(sub_parameter.router)