from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Receipt(Base):
    __tablename__ = "receipts"

    receipt_id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.sale_id"), nullable=False)
    receipt_number = Column(String(50), nullable=False, unique=True)
    issued_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    sale = relationship("Sale")

    def __repr__(self):
        return f"<Receipt(receipt_id={self.receipt_id}, receipt_number='{self.receipt_number}')>"
