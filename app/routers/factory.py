from typing import Type

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_roles
from app.database import get_db
from app.services.base import CRUDService


def build_crud_router(
    *,
    prefix: str,
    tags: list[str],
    service: CRUDService,
    create_schema: Type[BaseModel],
    update_schema: Type[BaseModel],
    read_schema: Type[BaseModel],
    write_roles: tuple[str, ...] = ("admin", "manager"),
) -> APIRouter:
    """Builds a standard authenticated-read / role-gated-write CRUD router.
    Any logged-in user can read; only the given roles can create/update/delete."""

    router = APIRouter(prefix=prefix, tags=tags)
    write_dependency = require_roles(*write_roles)

    @router.get("/", response_model=list[read_schema])
    def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _=Depends(get_current_user)):
        return service.list(db, skip, limit)

    @router.get("/{item_id}", response_model=read_schema)
    def get_item(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
        return service.get(db, item_id)

    @router.post("/", response_model=read_schema, status_code=status.HTTP_201_CREATED)
    def create_item(item: create_schema, db: Session = Depends(get_db), _=Depends(write_dependency)):
        return service.create(db, item.model_dump())

    @router.put("/{item_id}", response_model=read_schema)
    def update_item(item_id: int, item: update_schema, db: Session = Depends(get_db), _=Depends(write_dependency)):
        return service.update(db, item_id, item.model_dump(exclude_unset=True))

    @router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_item(item_id: int, db: Session = Depends(get_db), _=Depends(write_dependency)):
        service.delete(db, item_id)
        return None

    return router
