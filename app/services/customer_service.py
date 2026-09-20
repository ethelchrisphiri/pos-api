from app.repositories.customer import customer_repository
from app.services.base import CRUDService

customer_service = CRUDService(customer_repository, "Customer not found")
