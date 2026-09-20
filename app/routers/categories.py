from app.routers.factory import build_crud_router
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.category_service import category_service

router = build_crud_router(
    prefix="/categories",
    tags=["categories"],
    service=category_service,
    create_schema=CategoryCreate,
    update_schema=CategoryUpdate,
    read_schema=CategoryRead,
)
