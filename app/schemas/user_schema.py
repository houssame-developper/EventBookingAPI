from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from models import UserRole


class BaseUser(BaseModel):
    name: str
    email: EmailStr


class UserCreate(BaseUser):
    password: str
    role: Optional[UserRole] = None

class Register(BaseUser):
    password: str

class UserUpdate(BaseUser):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None


class UserRead(BaseUser):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    role: UserRole
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None


class Login(BaseModel):
    email: EmailStr
    password: str