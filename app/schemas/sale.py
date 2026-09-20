from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.sale_item import SaleItemCreate, SaleItemRead


class SaleCreate(BaseModel):
    customer_id: Optional[int] = None
    items: list[SaleItemCreate] = Field(min_length=1)


class SaleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sale_id: int
    sale_date: datetime
    customer_id: Optional[int]
    user_id: int
    total_amount: Decimal
    sale_items: list[SaleItemRead] = []
