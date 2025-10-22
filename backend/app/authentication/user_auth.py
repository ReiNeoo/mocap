import uuid
from typing import Any, Dict, Tuple

from sqlmodel import Session, select
from fastapi import HTTPException

from app.crud.user_ops import read_user_email
from app.crud import tenant_ops, user_ops
from app.core.security import verify_password, get_password_hash

from app.models import User, UserRole, RoleType, SubscriptionLevel


def authenticate(session: Session, email: str, password: str) -> User | None:
    db_user = read_user_email(session, email)
    if not db_user:
        return None
    if not verify_password(password, db_user.password_hash):
        return None
    return db_user


# SubscriptionLevel | Dict | None


def get_user_authorization(
    session: Session, user: User, user_role: UserRole
) -> SubscriptionLevel | Dict | None:
    role = user_role.role_type
    if role in (RoleType.STUDENT, RoleType.PARENT):
        if user.tenant_id:
            tenant_sub_plan = tenant_ops.read_tenant_sub_plan_by_id(
                session=session, tenant_id=user.tenant_id
            )
            return tenant_sub_plan.special_subscription_plan
        else:
            user_sub_plan = user_ops.read_user_sub_plan_by_id(session, user_id=user.id)
            if user_sub_plan and user_sub_plan.sub_level:
                return user_sub_plan.sub_level
            return SubscriptionLevel.FREE

    elif role in (RoleType.TEACHER, RoleType.COACH):
        return SubscriptionLevel.FREE

    elif role == RoleType.TENANT_ADMIN:
        tenant_sub_plan = tenant_ops.read_tenant_sub_plan_by_id(
            session=session, tenant_id=user.tenant_id
        )
        return tenant_sub_plan.special_subscription_plan
    elif role == RoleType.SUPER_ADMIN:
        return SubscriptionLevel.SUPER_ADMIN

    return None


# TODO:
#     kayıttan sonra kullanıcının rol ataması yapılmalı +
#     bunu için gerekli end-pointler yazılmalı +
#     ardından kullanıcı eğer öğrenciyse profil oluşturacak
#     sign-in için jwt token hazırlanmalı
