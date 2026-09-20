from datetime import timedelta

import pytest
from fastapi import HTTPException

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_password_returns_different_string():
    password = "testpassword123"
    hashed = hash_password(password)
    assert isinstance(hashed, str)
    assert hashed != password


def test_verify_password_success_and_failure():
    password = "testpassword123"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_create_and_decode_access_token():
    token = create_access_token({"sub": "alice", "role": "cashier"})
    assert isinstance(token, str)
    payload = decode_access_token(token)
    assert payload["sub"] == "alice"
    assert payload["role"] == "cashier"


def test_decode_expired_token_raises_401():
    token = create_access_token({"sub": "alice"}, expires_delta=timedelta(seconds=-1))
    with pytest.raises(HTTPException) as exc_info:
        decode_access_token(token)
    assert exc_info.value.status_code == 401


def test_decode_invalid_token_raises_401():
    with pytest.raises(HTTPException) as exc_info:
        decode_access_token("not-a-valid-token")
    assert exc_info.value.status_code == 401
