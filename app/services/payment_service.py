from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.payment import Payment, PaymentStatus
from app.models.sale import Sale
from app.repositories.payment import payment_repository


def create_payment(db: Session, sale_id: int, method: str, amount: Decimal) -> Payment:
    sale = db.query(Sale).filter(Sale.sale_id == sale_id).first()
    if sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")

    completed_payments = (
        db.query(Payment)
        .filter(Payment.sale_id == sale_id, Payment.status == PaymentStatus.COMPLETED)
        .all()
    )
    already_paid = sum((p.amount for p in completed_payments), Decimal("0"))
    remaining = sale.total_amount - already_paid

    if amount > remaining:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Payment amount exceeds the remaining balance of {remaining}",
        )

    return payment_repository.create(
        db,
        {"sale_id": sale_id, "method": method, "amount": amount, "status": PaymentStatus.COMPLETED},
    )


def get_payment(db: Session, payment_id: int) -> Payment:
    payment = payment_repository.get(db, payment_id)
    if payment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    return payment


def list_payments(db: Session, skip: int = 0, limit: int = 100):
    return payment_repository.get_all(db, skip, limit)


def update_payment_status(db: Session, payment_id: int, new_status: str) -> Payment:
    payment = get_payment(db, payment_id)
    payment.status = PaymentStatus(new_status)
    db.commit()
    db.refresh(payment)
    return payment
