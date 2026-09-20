from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReceiptCreate(BaseModel):
    sale_id: int


class ReceiptRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    receipt_id: int
    sale_id: int
    receipt_number: str
    issued_at: datetime
