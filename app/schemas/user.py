from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

Role = Literal["admin", "manager", "cashier"]


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=20)


class UserCreate(UserBase):
    # Note: role is intentionally NOT accepted here. Public registration
    # always creates a "cashier" account (see AuthService.register) so a
    # caller can't self-assign admin/manager privileges. Roles are only
    # changed afterwards by an existing admin via PUT /users/{id}.
    password: str = Field(min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        if not any(c.isdigit() for c in v) or not any(c.isalpha() for c in v):
            raise ValueError("Password must contain at least one letter and one number")
        return v


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[Role] = None
    is_active: Optional[bool] = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    role: Role
    is_active: bool
    # password_hash is deliberately never exposed here.
