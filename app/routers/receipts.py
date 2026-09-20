from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.schemas.receipt import ReceiptCreate, ReceiptRead
from app.services import receipt_service

router = APIRouter(prefix="/receipts", tags=["receipts"])


@router.get("/", response_model=list[ReceiptRead])
def list_receipts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return receipt_service.list_receipts(db, skip, limit)


@router.get("/{receipt_id}", response_model=ReceiptRead)
def get_receipt(receipt_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return receipt_service.get_receipt(db, receipt_id)


@router.post("/", response_model=ReceiptRead, status_code=status.HTTP_201_CREATED)
def create_receipt(receipt_in: ReceiptCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return receipt_service.create_receipt(db, receipt_in.sale_id)
