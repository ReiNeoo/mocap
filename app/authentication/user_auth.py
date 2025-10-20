import uuid
from typing import Any, Dict

from sqlmodel import Session, select
from fastapi import HTTPException


from app.crud.user_ops import read_user_email
from app.crud import tenant_ops
from app.core.security import verify_password, get_password_hash

from app.models import User, UserRole, RoleType


def authenticate(session: Session, email: str, password: str) -> User | None:
    db_user = read_user_email(session, email)
    if not db_user:
        return None
    if not verify_password(password, db_user.password_hash):
        return None
    return db_user


def get_user_authorization(
    session: Session, user: User, user_role: UserRole
) -> str | None:
    role = user_role.role_type
    if role in (RoleType.STUDENT, RoleType.PARENT):
        if user.tenant_id:
            tenant = tenant_ops.read_tenant_by_id(
                session=session, tenant_id=user.tenant_id
            )
            return tenant.subscription_plans
        else:
            return role

    elif role in (RoleType.TENANT_ADMIN, RoleType.SUPER_ADMIN):

        # tenant varlığı kontrol et

        return role

    return None


# TODO:
#     kayıttan sonra kullanıcının rol ataması yapılmalı +
#     bunu için gerekli end-pointler yazılmalı +
#     ardından kullanıcı eğer öğrenciyse profil oluşturacak
#     sign-in için jwt token hazırlanmalı
