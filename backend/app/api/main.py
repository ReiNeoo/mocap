from fastapi import APIRouter

from app.api.routes import login, users, tenants, utils
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(tenants.router)
api_router.include_router(utils.router)
