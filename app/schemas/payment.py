from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

PaymentMethod = Literal["cash", "card", "mobile", "bank_transfer"]
PaymentStatusLiteral = Literal["PENDING", "COMPLETED", "FAILED", "REFUNDED"]


class PaymentCreate(BaseModel):
    sale_id: int
    method: PaymentMethod
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class PaymentStatusUpdate(BaseModel):
    status: PaymentStatusLiteral


class PaymentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    payment_id: int
    sale_id: int
    method: str
    amount: Decimal
    status: str
    paid_at: datetime
