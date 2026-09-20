from app.routers.factory import build_crud_router
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product_service import product_service

router = build_crud_router(
    prefix="/products",
    tags=["products"],
    service=product_service,
    create_schema=ProductCreate,
    update_schema=ProductUpdate,
    read_schema=ProductRead,
)
