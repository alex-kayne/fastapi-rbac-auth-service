from app.repositories.users import UsersRepository
from app.services.auth import AuthService


def get_user_repository() -> UsersRepository:
    return UsersRepository()


def get_auth_service() -> AuthService:
    return AuthService(get_user_repository())
