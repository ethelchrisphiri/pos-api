from app.routers.factory import build_crud_router
from app.schemas.supplier import SupplierCreate, SupplierRead, SupplierUpdate
from app.services.supplier_service import supplier_service

router = build_crud_router(
    prefix="/suppliers",
    tags=["suppliers"],
    service=supplier_service,
    create_schema=SupplierCreate,
    update_schema=SupplierUpdate,
    read_schema=SupplierRead,
)
