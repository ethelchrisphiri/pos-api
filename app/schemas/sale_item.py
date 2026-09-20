from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    discount_amount: Decimal = Field(default=Decimal("0"), ge=0, max_digits=10, decimal_places=2)


class SaleItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sale_item_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    discount_amount: Decimal
    total_price: Decimal
