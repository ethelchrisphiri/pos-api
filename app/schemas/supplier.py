from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SupplierBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=20)
    email: Optional[EmailStr] = None


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class SupplierRead(SupplierBase):
    model_config = ConfigDict(from_attributes=True)

    supplier_id: int
