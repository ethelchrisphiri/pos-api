from typing import Generic, TypeVar

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.base import CRUDRepository

ModelType = TypeVar("ModelType")


class CRUDService(Generic[ModelType]):
    def __init__(self, repository: CRUDRepository, not_found_msg: str):
        self.repository = repository
        self.not_found_msg = not_found_msg

    def get(self, db: Session, id_: int) -> ModelType:
        obj = self.repository.get(db, id_)
        if obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=self.not_found_msg)
        return obj

    def list(self, db: Session, skip: int = 0, limit: int = 100):
        return self.repository.get_all(db, skip, limit)

    def create(self, db: Session, data: dict):
        return self.repository.create(db, data)

    def update(self, db: Session, id_: int, data: dict):
        obj = self.get(db, id_)
        return self.repository.update(db, obj, data)

    def delete(self, db: Session, id_: int) -> None:
        obj = self.get(db, id_)
        self.repository.delete(db, obj)
