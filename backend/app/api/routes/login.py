from typing import Any, Annotated
from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.crud import user_ops
from app.api.dependencies.db_deps import SessionDep
from app.authentication.user_auth import authenticate, get_user_authorization
from app.core.security import create_access_token
from app.core.config import settings

from app.models import Token


router = APIRouter(tags=["login"], prefix="/login")


@router.post("/access-token")
def get_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate(session, email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Account Disabled")

    user_role = user_ops.read_user_role(session=session, user_id=user.id)
    user_autherization = get_user_authorization(session, user, user_role)

    if not user_autherization:
        raise HTTPException(status_code=401, detail="User has no valid role")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    jwt_token = create_access_token(
        user_id=user.id,
        tenant_id=user.tenant_id,
        role=user_role.role_type,
        subscription_level=user_autherization,
        expire_delta=access_token_expires,
    )
    return Token(access_token=jwt_token)


# TODO:
#     get_user_authorization fonksiyonunun doğru dönüş yaptığından emin ol
