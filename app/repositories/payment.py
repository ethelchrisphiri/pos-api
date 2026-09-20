from app.models.payment import Payment
from app.repositories.base import CRUDRepository

payment_repository = CRUDRepository(Payment, "payment_id")
