import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Any, Dict

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel, JSON, Column
from sqlalchemy import Text


class SubscriptionLevel(str, Enum):
    FREE = "free"
    GOLD = "gold"
    PREMIUM = "premium"
    PRO = "pro"


class RoleType(str, Enum):
    STUDENT = "student"
    PARENT = "parent"
    TEACHER = "teacher"
    COACH = "coach"
    TENANT_ADMIN = "tenant_admin"
    SUPER_ADMIN = "super_admin"


class TenantBase(SQLModel):
    name: str = Field(max_length=255)
    max_users: Optional[int] = Field(default=None)
    mongodb_database_name: Optional[str] = Field(default=None, max_length=255)
    firebase_config: Optional[Dict[str, Any]] = Field(
        default=None, sa_column=Column(JSON)
    )
    is_active: bool = Field(default=True)
    is_payed: bool = Field(default=False)
    city: Optional[str] = Field(default=None, max_length=255)
    district: Optional[str] = Field(default=None, max_length=255)
    address: Optional[str] = Field(default=None, sa_column=Column(Text))
    VKN_code: Optional[str] = Field(default=None, max_length=10)


class TenantCreate(TenantBase):
    pass


class TenantUpdate(SQLModel):
    name: Optional[str] = Field(default=None, max_length=255)
    domain: Optional[str] = Field(default=None, max_length=255)
    address: Optional[str] = Field(default=None)
    max_users: Optional[int] = Field(default=None)
    mongodb_database_name: Optional[str] = Field(default=None, max_length=255)
    firebase_config: Optional[Dict[str, Any]] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)
    is_payed: Optional[bool] = Field(default=None)
    city: Optional[str] = Field(default=None, max_length=255)
    district: Optional[str] = Field(default=None, max_length=255)


class Tenant(TenantBase, table=True):
    __tablename__ = "tenants"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    users: List["User"] = Relationship(back_populates="tenant", cascade_delete=True)
    subscription_plans: List["TenantSubscriptionPlan"] = Relationship(
        back_populates="tenant", cascade_delete=True
    )
    user_roles: List["UserRole"] = Relationship(
        back_populates="tenant", cascade_delete=True
    )


class TenantPublic(TenantBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class TenantSubscriptionPlanBase(SQLModel):
    special_subscription_plan: Optional[Dict[str, Any]] = Field(
        default=None, sa_column=Column(JSON)
    )
    subscription_fee: Optional[Decimal] = Field(
        default=None, max_digits=10, decimal_places=2
    )
    starts_at: Optional[datetime] = Field(default=None)
    ends_at: Optional[datetime] = Field(default=None)
    is_active: bool = Field(default=True)


class TenantSubscriptionPlan(TenantSubscriptionPlanBase, table=True):
    __tablename__ = "tenant_subscription_plan"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    tenant_id: uuid.UUID = Field(foreign_key="tenants.id", nullable=False)

    # Relationships
    tenant: Optional[Tenant] = Relationship(back_populates="subscription_plans")


class TenantSubscriptionPlanCreate(TenantBase):
    pass


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    first_name: Optional[str] = Field(default=None, max_length=255)
    last_name: Optional[str] = Field(default=None, max_length=255)
    turkish_identification_number: Optional[str] = Field(
        default=None, max_length=11, unique=True
    )
    avatar_url: Optional[str] = Field(default=None, sa_column=Column(Text))
    firebase_uid: Optional[str] = Field(default=None, max_length=255, unique=True)
    email_verified: bool = Field(default=False)
    is_active: bool = Field(default=True)
    phone: Optional[str] = Field(default=None, max_length=20)
    city: Optional[str] = Field(default=None, max_length=255)
    district: Optional[str] = Field(default=None, max_length=255)
    address: Optional[str] = Field(default=None, sa_column=Column(Text))


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)
    tenant_id: Optional[uuid.UUID]


class UserUpdate(SQLModel):
    email: Optional[EmailStr] = Field(default=None, max_length=255)
    password: Optional[str] = Field(default=None, min_length=8, max_length=40)
    tenant_id: Optional[uuid.UUID]
    first_name: Optional[str] = Field(default=None, max_length=255)
    last_name: Optional[str] = Field(default=None, max_length=255)
    turkish_identification_number: Optional[str] = Field(default=None, max_length=11)
    avatar_url: Optional[str] = Field(default=None)
    firebase_uid: Optional[str] = Field(default=None, max_length=255)
    email_verified: Optional[bool] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)
    phone: Optional[str] = Field(default=None, max_length=20)
    city: Optional[str] = Field(default=None, max_length=255)
    district: Optional[str] = Field(default=None, max_length=255)
    address: Optional[str] = Field(default=None)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    tenant_id: Optional[uuid.UUID] = Field(foreign_key="tenants.id", nullable=True)
    password_hash: str = Field(max_length=255)
    last_login: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tenant: Optional[Tenant] = Relationship(back_populates="users")
    subscription_plans: List["UserSubscriptionPlan"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    roles: List["UserRole"] = Relationship(back_populates="user", cascade_delete=True)
    student_profile: Optional["StudentProfile"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    parent_relations: List["ParentStudentRelation"] = Relationship(
        back_populates="parent",
        sa_relationship_kwargs={"foreign_keys": "ParentStudentRelation.parent_id"},
        cascade_delete=True,
    )
    student_relations: List["ParentStudentRelation"] = Relationship(
        back_populates="student",
        sa_relationship_kwargs={"foreign_keys": "ParentStudentRelation.student_id"},
        cascade_delete=True,
    )


class UserPublic(UserBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime


# User Subscription Plan Models
class UserSubscriptionPlanBase(SQLModel):
    setting_fee: Optional[Decimal] = Field(
        default=None, max_digits=10, decimal_places=2
    )
    sub_level: Optional[SubscriptionLevel] = Field(default=None)
    is_active: bool = Field(default=True)
    starts_at: Optional[datetime] = Field(default=None)
    ends_at: Optional[datetime] = Field(default=None)


class UserSubscriptionPlanCreate(UserSubscriptionPlanBase):
    user_id: uuid.UUID


class UserSubscriptionPlan(UserSubscriptionPlanBase, table=True):
    __tablename__ = "user_subscription_plan"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)

    # Relationships
    user: Optional[User] = Relationship(back_populates="subscription_plans")


# User Roles Models
class UserRoleBase(SQLModel):
    role_type: RoleType = Field(max_length=50)


class UserRoleCreate(UserRoleBase):
    user_id: Optional[uuid.UUID]
    tenant_id: Optional[uuid.UUID]


class UserRole(UserRoleBase, table=True):
    __tablename__ = "user_roles"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    tenant_id: Optional[uuid.UUID] = Field(foreign_key="tenants.id", nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional[User] = Relationship(back_populates="roles")
    tenant: Optional[Tenant] = Relationship(back_populates="user_roles")


class UserRolePublic(UserRoleBase):
    id: uuid.UUID
    user_id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime


# Student Profile Models
class StudentProfileBase(SQLModel):
    grade_level: Optional[str] = Field(default=None, max_length=20)
    school_name: Optional[str] = Field(default=None, max_length=255)
    target_school: Optional[str] = Field(default=None, max_length=255)
    available_study_times: Optional[Dict[str, Any]] = Field(
        default=None, sa_column=Column(JSON)
    )
    school_lecture_program: Optional[Dict[str, Any]] = Field(
        default=None, sa_column=Column(JSON)
    )


class StudentProfileCreate(StudentProfileBase):
    user_id: uuid.UUID


class StudentProfile(StudentProfileBase, table=True):
    __tablename__ = "student_profiles"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)

    # Relationships
    user: Optional[User] = Relationship(back_populates="student_profile")


class StudentProfilePublic(StudentProfileBase):
    id: uuid.UUID
    user_id: uuid.UUID


# Parent-Student Relations Models
class ParentStudentRelationBase(SQLModel):
    pass


class ParentStudentRelationCreate(ParentStudentRelationBase):
    parent_id: uuid.UUID
    student_id: uuid.UUID


class ParentStudentRelation(ParentStudentRelationBase, table=True):
    __tablename__ = "parent_student_relations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    parent_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    student_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)

    # Relationships
    parent: Optional[User] = Relationship(
        back_populates="parent_relations",
        sa_relationship_kwargs={"foreign_keys": "[ParentStudentRelation.parent_id]"},
    )
    student: Optional[User] = Relationship(
        back_populates="student_relations",
        sa_relationship_kwargs={"foreign_keys": "[ParentStudentRelation.student_id]"},
    )


class ParentStudentRelationPublic(ParentStudentRelationBase):
    id: uuid.UUID
    parent_id: uuid.UUID
    student_id: uuid.UUID


# Response Models
class TenantsPublic(SQLModel):
    data: List[TenantPublic]
    count: int


class UsersPublic(SQLModel):
    data: List[UserPublic]
    count: int


class UserRolesPublic(SQLModel):
    data: List[UserRolePublic]
    count: int


class StudentProfilesPublic(SQLModel):
    data: List[StudentProfilePublic]
    count: int


class ParentStudentRelationsPublic(SQLModel):
    data: List[ParentStudentRelationPublic]
    count: int


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
