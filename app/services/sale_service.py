from decimal import Decimal
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.repositories.sale import sale_repository


def create_sale(db: Session, current_user_id: int, customer_id: Optional[int], items: list[dict]) -> Sale:
    if not items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A sale must include at least one item")

    sale_items: list[SaleItem] = []
    total_amount = Decimal("0")

    # NOTE: for a production Postgres deployment under real concurrency,
    # wrap this in `SELECT ... FOR UPDATE` (or a SERIALIZABLE transaction)
    # on each Product row so two simultaneous sales can't both pass the
    # stock check for the last unit. SQLite (used here/in tests) doesn't
    # support row locking, so we keep it simple and rely on the single
    # commit at the end to catch gross inconsistencies.
    for item in items:
        product = db.query(Product).filter(Product.product_id == item["product_id"]).first()
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item['product_id']} not found",
            )

        quantity = item["quantity"]
        discount = item.get("discount_amount", Decimal("0"))

        if product.stock_qty < quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product '{product.name}'",
            )

        line_total = (product.price * quantity) - discount
        if line_total < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Discount cannot exceed the item's subtotal",
            )

        product.stock_qty -= quantity
        total_amount += line_total

        sale_items.append(
            SaleItem(
                product_id=product.product_id,
                quantity=quantity,
                unit_price=product.price,
                discount_amount=discount,
                total_price=line_total,
            )
        )

    sale = Sale(
        customer_id=customer_id,
        user_id=current_user_id,
        total_amount=total_amount,
        sale_items=sale_items,
    )
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale


def get_sale(db: Session, sale_id: int) -> Sale:
    sale = sale_repository.get(db, sale_id)
    if sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")
    return sale


def list_sales(db: Session, skip: int = 0, limit: int = 100):
    return sale_repository.get_all(db, skip, limit)
