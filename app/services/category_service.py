from app.repositories.category import category_repository
from app.services.base import CRUDService

category_service = CRUDService(category_repository, "Category not found")
