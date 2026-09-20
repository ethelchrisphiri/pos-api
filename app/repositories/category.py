from app.models.category import Category
from app.repositories.base import CRUDRepository

category_repository = CRUDRepository(Category, "category_id")
