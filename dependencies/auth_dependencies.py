from fastapi import Depends

from dependencies.user_dependencies import get_user_repository
from repositories.user_repository import UserRepository
from service.auth_service import AuthService


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repo)