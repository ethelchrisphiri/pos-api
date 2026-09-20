from collections import defaultdict
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.users import users_repository

# A hash of a password nobody will ever type, used so failed-login
# timing doesn't reveal whether a username exists (verify_password is
# always run, even when there's no matching user).
_DUMMY_HASH = hash_password("this-is-not-a-real-password-!!")


class AuthService:
    def __init__(self):
        # In-memory brute-force tracker, keyed by username. Fine for a
        # single-process deployment; move to Redis (or similar shared
        # store) if you run multiple workers/instances.
        self._failed_attempts: dict[str, list[datetime]] = defaultdict(list)

    def register(self, db: Session, user_data: dict):
        if users_repository.get_by_username(db, user_data["username"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

        email = user_data.get("email")
        if email and users_repository.get_by_email(db, email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        plain_password = user_data.pop("password")
        user_data["password_hash"] = hash_password(plain_password)
        # Registration can never grant elevated roles - always cashier.
        # Promoting to manager/admin is an admin-only action afterwards.
        user_data["role"] = "cashier"

        return users_repository.create(db, user_data)

    def authenticate(self, db: Session, username: str, password: str) -> dict:
        self._check_lockout(username)

        user = users_repository.get_by_username(db, username) or users_repository.get_by_email(db, username)
        password_hash = user.password_hash if user else _DUMMY_HASH
        password_valid = verify_password(password, password_hash)

        if not user or not password_valid or not user.is_active:
            self._record_failure(username)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        self._clear_failures(username)
        user.last_login = datetime.now(timezone.utc)
        db.commit()

        access_token = create_access_token({"sub": user.username, "role": user.role})
        return {"access_token": access_token, "token_type": "bearer"}

    def _check_lockout(self, key: str) -> None:
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(minutes=settings.login_lockout_minutes)
        attempts = [t for t in self._failed_attempts[key] if t > window_start]
        self._failed_attempts[key] = attempts
        if len(attempts) >= settings.max_login_attempts:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many failed login attempts. Please try again later.",
            )

    def _record_failure(self, key: str) -> None:
        self._failed_attempts[key].append(datetime.now(timezone.utc))

    def _clear_failures(self, key: str) -> None:
        self._failed_attempts.pop(key, None)


auth_service = AuthService()
