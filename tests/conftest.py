import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401
from app.core.security import hash_password
from app.database import Base, get_db
from app.main import app
from app.models.user import User

TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def admin_header(client, db_session):
    # Mirrors app/scripts/create_admin.py: admins are seeded directly, never
    # created through the public registration endpoint.
    admin = User(
        username="admin_user",
        email="admin@example.com",
        password_hash=hash_password("StrongPass1"),
        role="admin",
        is_active=True,
    )
    db_session.add(admin)
    db_session.commit()

    response = client.post("/auth/login", json={"username": "admin_user", "password": "StrongPass1"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def cashier_header(client):
    client.post(
        "/auth/register",
        data={"username": "cashier_user", "email": "cashier@example.com", "password": "StrongPass1"},
    )
    response = client.post("/auth/login", json={"username": "cashier_user", "password": "StrongPass1"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
