from fastapi import APIRouter
from app.endpoints import employee

router = APIRouter()
router.include_router(employee.router)