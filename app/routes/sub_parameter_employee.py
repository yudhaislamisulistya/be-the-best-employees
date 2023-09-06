from fastapi import APIRouter
from app.endpoints import sub_parameter_employee

router = APIRouter()
router.include_router(sub_parameter_employee.router)