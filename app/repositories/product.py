from app.models.product import Product
from app.repositories.base import CRUDRepository

product_repository = CRUDRepository(Product, "product_id")
