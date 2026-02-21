from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.user import UserRole


# -------------------------
# Base Schema
# -------------------------
class UserBase(BaseModel):
    email: EmailStr


# -------------------------
# Create User
# -------------------------
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role: UserRole


# -------------------------
# Login Schema
# -------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# -------------------------
# Response Schema
# -------------------------
class UserResponse(UserBase):
    id: UUID
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Token Schemas
# -------------------------
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[UUID] = None