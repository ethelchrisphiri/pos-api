from app.models.receipt import Receipt
from app.repositories.base import CRUDRepository

receipt_repository = CRUDRepository(Receipt, "receipt_id")
