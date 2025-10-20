import json

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.crud import user_ops
from app.core.security import get_password_hash
from app.api.dependencies.db_deps import SessionDep

from app.models import User, UserCreate, UserPublic, UserRoleCreate

router = APIRouter(tags=["users"], prefix="/users")


# TODO:
@router.get("/")
def get_user():
    pass


# TODO:
@router.get("/{user_id}")
def get_users():
    pass


@router.post("/", response_model=UserPublic)
def create_user(
    *, session: SessionDep, user_in: UserCreate, role_in: UserRoleCreate
) -> Any:
    existing_user = user_ops.read_user_email(session, email=user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User Exists")

    user = user_ops.create_user(session, user_in)
    user_ops.create_user_role(session, user=user, role_in=role_in)
    return user
