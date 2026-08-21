from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from dependencies.user_dependencies import get_user_repository
from repositories.user_repository import UserRepository
from service.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repo)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: AuthService = Depends(get_auth_service),
):
    return service.get_current_user(token)
