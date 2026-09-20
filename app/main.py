from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import models  # noqa: F401  (registers every model on Base.metadata)
from app.database import Base, engine
from app.routers import (
    auth,
    categories,
    customers,
    payments,
    products,
    receipts,
    sale_items,
    sales,
    suppliers,
    users,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="POS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # Never leak stack traces / internals to the client.
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(suppliers.router)
app.include_router(customers.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(sales.router)
app.include_router(sale_items.router)
app.include_router(payments.router)
app.include_router(receipts.router)


@app.get("/")
def root():
    return {"message": "POS API is running"}
