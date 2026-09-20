from typing import Generic, TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class CRUDRepository(Generic[ModelType]):
    """Generic data-access layer shared by every entity. Keeps the same
    get/get_all/create/update/delete shape you already had in
    category_repository.py, without repeating it nine times."""

    def __init__(self, model: type[ModelType], pk_field: str):
        self.model = model
        self.pk_field = pk_field

    def get(self, db: Session, id_: int):
        return db.query(self.model).filter(getattr(self.model, self.pk_field) == id_).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, data: dict):
        obj = self.model(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: ModelType, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: ModelType) -> None:
        db.delete(db_obj)
        db.commit()
