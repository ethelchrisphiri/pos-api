from app.models.sale import Sale
from app.repositories.base import CRUDRepository

sale_repository = CRUDRepository(Sale, "sale_id")
