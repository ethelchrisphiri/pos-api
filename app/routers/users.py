from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_roles
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate
from app.services.user_service import user_service

router = APIRouter(prefix="/users", tags=["users"])
admin_only = require_roles("admin")


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=list[UserRead])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _=Depends(admin_only)):
    return user_service.list(db, skip, limit)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db), _=Depends(admin_only)):
    return user_service.get(db, user_id)


@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db), _=Depends(admin_only)):
    return user_service.update(db, user_id, user_in.model_dump(exclude_unset=True))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), _=Depends(admin_only)):
    user_service.delete(db, user_id)
    return None
