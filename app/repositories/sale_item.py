from app.models.sale_item import SaleItem
from app.repositories.base import CRUDRepository

sale_item_repository = CRUDRepository(SaleItem, "sale_item_id")
