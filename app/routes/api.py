from fastapi import APIRouter
from .user import router as user_router
from .employee import router as employee_router
from .parameter import router as parameter_router
from .sub_parameter import router as sub_parameter_router
from .grade_sub_parameter import router as grade_sub_parameter_router
from .sub_parameter_employee import router as sub_parameter_employee_router
from .batch import router as batch_router
from .preference_type import router as preference_type_router
from .ranking import router as ranking_router

router = APIRouter()
router.include_router(user_router)
router.include_router(employee_router)
router.include_router(parameter_router)
router.include_router(sub_parameter_router)
router.include_router(grade_sub_parameter_router)
router.include_router(sub_parameter_employee_router)
router.include_router(batch_router)
router.include_router(preference_type_router)
router.include_router(ranking_router)
