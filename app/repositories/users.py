from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base import CRUDRepository


class UserRepository(CRUDRepository[User]):
    def __init__(self):
        super().__init__(User, "user_id")

    def get_by_username(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()


users_repository = UserRepository()
