from app.repositories.users import users_repository
from app.services.base import CRUDService

user_service = CRUDService(users_repository, "User not found")
