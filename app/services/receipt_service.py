import secrets

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.receipt import Receipt
from app.models.sale import Sale
from app.repositories.receipt import receipt_repository


def create_receipt(db: Session, sale_id: int) -> Receipt:
    sale = db.query(Sale).filter(Sale.sale_id == sale_id).first()
    if sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")

    receipt_number = f"RCT-{sale_id}-{secrets.token_hex(4).upper()}"
    return receipt_repository.create(db, {"sale_id": sale_id, "receipt_number": receipt_number})


def get_receipt(db: Session, receipt_id: int) -> Receipt:
    receipt = receipt_repository.get(db, receipt_id)
    if receipt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")
    return receipt


def list_receipts(db: Session, skip: int = 0, limit: int = 100):
    return receipt_repository.get_all(db, skip, limit)
