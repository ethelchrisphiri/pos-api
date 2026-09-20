from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    stock_qty: int = Field(ge=0)
    category_id: int
    supplier_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    price: Optional[Decimal] = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    stock_qty: Optional[int] = Field(default=None, ge=0)
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
