from app.api.routes.endpoints import user
from fastapi import APIRouter

router = APIRouter()
router.include_router(user.router)
