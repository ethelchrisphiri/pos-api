from app.models.customer import Customer
from app.repositories.base import CRUDRepository

customer_repository = CRUDRepository(Customer, "customer_id")
