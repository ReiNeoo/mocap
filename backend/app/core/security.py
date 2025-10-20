from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status


from app.core.config import settings
from app.core.constants import SUBSCRIPTION_FEATURES
from app.models import UserRole, RoleType, SubscriptionLevel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_jwt_payload(
    user_id: str,
    tenant_id: str,
    role: str,
    subscription_level: SubscriptionLevel,
    expire_timestamp: int,
):
    now = datetime.utcnow()
    return {
        "sub": user_id,
        "tenant_id": tenant_id,
        "role": role,
        "sub_plan": SUBSCRIPTION_FEATURES[subscription_level],
        "exp": expire_timestamp,
        "iat": int(now.timestamp()),
    }


def create_access_token(
    user_id: str,
    tenant_id: str,
    role: str,
    subscription_level: SubscriptionLevel,
    expire_delta: timedelta,
):
    try:
        expire = datetime.now(timezone.utc) + expire_delta
        token_payload = create_jwt_payload(
            user_id, tenant_id, role, subscription_level, expire
        )
        encoded_jwt = jwt.encode(
            token_payload, settings.SECRET_KEY, algorithm=ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        print(f"Error occured while creating Access Token: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create access token: {str(e)}",
        )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
