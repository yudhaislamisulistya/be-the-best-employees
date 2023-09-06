from fastapi import APIRouter
from app.endpoints import grade_sub_parameter

router = APIRouter()
router.include_router(grade_sub_parameter.router)