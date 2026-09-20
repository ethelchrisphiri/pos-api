from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)

    products = relationship("Product", back_populates="supplier")

    def __repr__(self):
        return f"<Supplier(supplier_id={self.supplier_id}, name='{self.name}')>"
