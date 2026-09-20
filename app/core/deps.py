from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database import get_db
from app.models.user import User
from app.repositories.users import users_repository

# tokenUrl is only used to populate API docs; /auth/login itself accepts a
# JSON body rather than an OAuth2 form, which is fine because this bearer
# scheme only extracts the "Authorization: Bearer <token>" header.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=True)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    username = payload.get("sub")
    if username is None:
        raise credentials_error

    user = users_repository.get_by_username(db, username)
    if user is None:
        raise credentials_error
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")

    return user


def require_roles(*roles: str):
    """Dependency factory: restricts a route to the given roles."""

    def dependency(current_user: Annotated[User, Depends(get_current_user)]) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )
        return current_user

    return dependency
