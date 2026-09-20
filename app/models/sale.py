from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Sale(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True, index=True)
    sale_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=True)
   
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False, default=0)

    customer = relationship("Customer")
    user = relationship("User")
    sale_items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Sale(sale_id={self.sale_id}, total_amount={self.total_amount})>"
