from app.repositories.product import product_repository
from app.services.base import CRUDService

product_service = CRUDService(product_repository, "Product not found")
