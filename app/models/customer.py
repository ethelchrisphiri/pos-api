from sqlalchemy import Column, Integer, String

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)

    def __repr__(self):
        return f"<Customer(customer_id={self.customer_id}, name='{self.name}')>"
