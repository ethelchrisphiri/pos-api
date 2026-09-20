from app.models.supplier import Supplier
from app.repositories.base import CRUDRepository

supplier_repository = CRUDRepository(Supplier, "supplier_id")
