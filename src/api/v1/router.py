from fastapi import APIRouter

from .auth import router as auth_router
from .dashboard import router as dashboard_router

router = APIRouter(prefix="/v1")
router.include_router(auth_router, prefix="/auth")
router.include_router(dashboard_router, prefix="/dashboard")
