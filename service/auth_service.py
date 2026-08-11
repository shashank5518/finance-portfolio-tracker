from exceptions.auth_exceptions import InvalidCredentialsError
from repositories.user_repository import UserRepository
from schemas.auth import TokenResponse
from utils.security import verify_password


class AuthService:

    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    def login(self, email: str, password: str,):
        user = self.user_repo.find_by_email(email)

        if user is None:
            raise InvalidCredentialsError("Invalid email or password.")

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError("Invalid email or password.")

        access_token = create_access_token(user.id)

        return TokenResponse(
            access_token = access_token,
            token_type = "bearer",
        )