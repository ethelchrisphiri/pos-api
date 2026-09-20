from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock_qty = Column(Integer, nullable=False, default=0)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.supplier_id"), nullable=False)

    category = relationship("Category", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")

    def __repr__(self):
        return f"<Product(product_id={self.product_id}, name='{self.name}')>"
