from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.sale import SaleCreate, SaleRead
from app.services import sale_service

router = APIRouter(prefix="/sales", tags=["sales"])


@router.get("/", response_model=list[SaleRead])
def list_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return sale_service.list_sales(db, skip, limit)


@router.get("/{sale_id}", response_model=SaleRead)
def get_sale(sale_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return sale_service.get_sale(db, sale_id)


@router.post("/", response_model=SaleRead, status_code=status.HTTP_201_CREATED)
def create_sale(
    sale_in: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return sale_service.create_sale(
        db,
        current_user_id=current_user.user_id,
        customer_id=sale_in.customer_id,
        items=[item.model_dump() for item in sale_in.items],
    )
