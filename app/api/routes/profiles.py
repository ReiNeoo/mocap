from typing import Any

from fastapi import APIRouter, HTTPException

from app.crud import user_ops
from app.core.security import get_password_hash
from app.api.dependencies.db_deps import SessionDep

from app.models import UserRoleCreate

router = APIRouter(tags=["profiles"], prefix="/profiles")


@router.post("/")
def create_student_profile(session: SessionDep, user_in: UserRoleCreate):
    pass
