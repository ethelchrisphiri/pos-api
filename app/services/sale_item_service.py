from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.sale_item import sale_item_repository

# Sale items are created as part of creating a Sale (see sale_service.py) so
# stock decrements and totals stay consistent. This service intentionally
# does NOT expose create/update - only read and an admin/manager-only
# delete for correcting mistakes.


def get_sale_item(db: Session, sale_item_id: int):
    sale_item = sale_item_repository.get(db, sale_item_id)
    if not sale_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale item not found")
    return sale_item


def list_sale_items(db: Session, skip: int = 0, limit: int = 100):
    return sale_item_repository.get_all(db, skip, limit)


def delete_sale_item(db: Session, sale_item_id: int) -> None:
    sale_item = get_sale_item(db, sale_item_id)
    sale_item_repository.delete(db, sale_item)
