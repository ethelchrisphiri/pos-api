from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_roles
from app.database import get_db
from app.schemas.sale_item import SaleItemRead
from app.services import sale_item_service

router = APIRouter(prefix="/sale-items", tags=["sale-items"])
manage = require_roles("admin", "manager")


@router.get("/", response_model=list[SaleItemRead])
def list_sale_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return sale_item_service.list_sale_items(db, skip, limit)


@router.get("/{sale_item_id}", response_model=SaleItemRead)
def get_sale_item(sale_item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return sale_item_service.get_sale_item(db, sale_item_id)


@router.delete("/{sale_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale_item(sale_item_id: int, db: Session = Depends(get_db), _=Depends(manage)):
    sale_item_service.delete_sale_item(db, sale_item_id)
    return None
