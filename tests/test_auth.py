from app.models.user import User


def test_register_new_user(client):
    response = client.post(
        "/auth/register",
        json={"username": "newuser", "email": "newuser@example.com", "password": "StrongPass1"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "newuser"
    assert body["role"] == "cashier"
    assert "password" not in body
    assert "password_hash" not in body


def test_register_duplicate_username_rejected(client):
    payload = {"username": "dupe", "email": "dupe@example.com", "password": "StrongPass1"}
    client.post("/auth/register", json=payload)
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400


def test_register_weak_password_rejected(client):
    response = client.post(
        "/auth/register",
        json={"username": "weakpw", "email": "weak@example.com", "password": "alllettersnodigits"},
    )
    assert response.status_code == 422


def test_register_ignores_role_escalation_attempt(client, db_session):
    client.post(
        "/auth/register",
        json={
            "username": "sneaky",
            "email": "sneaky@example.com",
            "password": "StrongPass1",
            "role": "admin",
        },
    )
    user = db_session.query(User).filter(User.username == "sneaky").first()
    assert user.role == "cashier"


def test_login_success(client):
    client.post("/auth/register", json={"username": "loginuser", "email": "l@example.com", "password": "StrongPass1"})
    response = client.post("/auth/login", json={"username": "loginuser", "password": "StrongPass1"})
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert "access_token" in body


def test_login_wrong_password(client):
    client.post("/auth/register", json={"username": "loginuser2", "email": "l2@example.com", "password": "StrongPass1"})
    response = client.post("/auth/login", json={"username": "loginuser2", "password": "WrongPass1"})
    assert response.status_code == 401


def test_login_lockout_after_repeated_failures(client):
    client.post("/auth/register", json={"username": "lockme", "email": "lk@example.com", "password": "StrongPass1"})
    for _ in range(5):
        client.post("/auth/login", json={"username": "lockme", "password": "WrongPass1"})
    response = client.post("/auth/login", json={"username": "lockme", "password": "StrongPass1"})
    assert response.status_code == 429


def test_protected_route_requires_token(client):
    response = client.get("/products/")
    assert response.status_code == 401