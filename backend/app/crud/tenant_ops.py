import uuid
from typing import Any

from sqlmodel import Session, select

from app.models import (
    Tenant,
    TenantCreate,
    TenantSubscriptionPlan,
    TenantSubscriptionPlanCreate,
)


def tenant_create(session: Session, tenant_create: TenantCreate) -> Tenant:
    db_object = Tenant.model_validate(tenant_create)

    session.add(db_object)
    session.commit()
    session.refresh(db_object)
    return db_object


def read_tenant_by_VKN(session: Session, tenant_vkn: str):
    statement = select(Tenant).where(Tenant.VKN_code == tenant_vkn)
    session_user = session.exec(statement).first()
    return session_user


def read_tenant_by_id(session: Session, tenant_id: uuid.UUID):
    statement = select(Tenant).where(Tenant.id == tenant_id)
    session_user = session.exec(statement).first()
    return session_user


def creat_tenant_sub_plan(
    session: Session, tenant_id: uuid.UUID, tenant_in: TenantSubscriptionPlanCreate
) -> TenantSubscriptionPlan:
    db_object = TenantSubscriptionPlan.model_validate(
        tenant_in, update={"tenant_id": tenant_id}
    )

    session.add(db_object)
    session.commit()
    session.refresh(db_object)
    return db_object


def read_tenant_sub_plan_by_id(
    session: Session, tenant_id: uuid.UUID
) -> TenantSubscriptionPlan | None:
    statement = select(TenantSubscriptionPlan).where(
        TenantSubscriptionPlan.tenant_id == tenant_id,
        TenantSubscriptionPlan.is_active == True,
    )
    session_user = session.exec(statement).first()
    return session_user
