from app.routers.factory import build_crud_router
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate
from app.services.customer_service import customer_service

router = build_crud_router(
    prefix="/customers",
    tags=["customers"],
    service=customer_service,
    create_schema=CustomerCreate,
    update_schema=CustomerUpdate,
    read_schema=CustomerRead,
    write_roles=("admin", "manager", "cashier"),
)
