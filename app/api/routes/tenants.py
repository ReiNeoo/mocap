from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.crud import user_ops, tenant_ops
from app.api.dependencies.db_deps import SessionDep

from app.models import Tenant, TenantPublic, TenantCreate

router = APIRouter(tags=["tenants"], prefix="/tenants")


# TODO:
#     Add users VKN confirmation system


@router.post("/", response_model=TenantPublic)
def create_tenant(*, session: SessionDep, tenant_in=TenantCreate) -> Any:
    existing_tenant = tenant_ops.read_tenant_by_VKN(
        session, tenant_vkn=tenant_in.VKN_code
    )
    if existing_tenant:
        raise HTTPException(status_code=400, detail="Tenant Exists")

    tenant = tenant_ops.tenant_create(session=session, tenant_create=tenant_in)
    return tenant
