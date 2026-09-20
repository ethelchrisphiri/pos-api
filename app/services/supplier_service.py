from app.repositories.supplier import supplier_repository
from app.services.base import CRUDService

supplier_service = CRUDService(supplier_repository, "Supplier not found")
