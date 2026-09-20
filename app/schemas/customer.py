from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=20)
    email: Optional[EmailStr] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class CustomerRead(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    customer_id: int
