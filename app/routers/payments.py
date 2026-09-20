from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_roles
from app.database import get_db
from app.schemas.payment import PaymentCreate, PaymentRead, PaymentStatusUpdate
from app.services import payment_service

router = APIRouter(prefix="/payments", tags=["payments"])
# Only admin/manager can move a payment into REFUNDED/FAILED etc - a
# cashier can take a payment but can't authorize their own refund.
manage_payments = require_roles("admin", "manager")


@router.get("/", response_model=list[PaymentRead])
def list_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return payment_service.list_payments(db, skip, limit)


@router.get("/{payment_id}", response_model=PaymentRead)
def get_payment(payment_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return payment_service.get_payment(db, payment_id)


@router.post("/", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
def create_payment(payment_in: PaymentCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return payment_service.create_payment(db, payment_in.sale_id, payment_in.method, payment_in.amount)


@router.patch("/{payment_id}/status", response_model=PaymentRead)
def update_payment_status(
    payment_id: int,
    status_in: PaymentStatusUpdate,
    db: Session = Depends(get_db),
    _=Depends(manage_payments),
):
    return payment_service.update_payment_status(db, payment_id, status_in.status)
