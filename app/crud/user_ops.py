import uuid
from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import (
    User,
    UserCreate,
    UserPublic,
    UserRoleCreate,
    UserRole,
    UserSubscriptionPlan,
    UserSubscriptionPlanCreate,
)


def create_user(session: Session, user_create: UserCreate) -> User:
    db_object = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )

    session.add(db_object)
    session.commit()
    session.refresh(db_object)
    return db_object


def read_user_email(session: Session, email: str) -> User:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def create_user_role(session: Session, user: User, role_in: UserRoleCreate) -> UserRole:
    db_object = UserRole.model_validate(
        role_in, update={"user_id": user.id, "tenant_id": user.tenant_id}
    )

    session.add(db_object)
    session.commit()
    session.refresh(db_object)
    return db_object


def read_user_role(session: Session, user_id: uuid.UUID) -> UserRole:
    statement = select(UserRole).where(UserRole.user_id == user_id)
    session_userrole = session.exec(statement).first()
    return session_userrole


def creat_user_sub_plan(
    session: Session, user_id: uuid.UUID, user_in: UserSubscriptionPlanCreate
) -> UserSubscriptionPlan:
    db_object = UserSubscriptionPlan.model_validate(
        user_in, update={"user_id": user_id}
    )

    session.add(db_object)
    session.commit()
    session.refresh(db_object)
    return db_object
