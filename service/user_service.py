from collections.abc import Sequence

from exceptions.user_service_exceptions import (
    DuplicateEmailError,
    DuplicatePhoneError,
    UserNotFoundError,
)
from repositories.user_repository import User, UserRepository
from schemas.user import UserCreate, UserUpdate
from utils.security import hash_password


class UserService:

    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    def create_user(self, user_data: UserCreate) -> User:
        if self.user_repo.exists_by_email(user_data.email):
            raise DuplicateEmailError(f"Email: {user_data.email} already exists")
        if self.user_repo.exists_by_phone(user_data.phone):
            raise DuplicatePhoneError(f"Phone: {user_data.phone} already exists")
        user = User(
            name=user_data.name,
            email=user_data.email,
            phone=user_data.phone,
            password_hash=hash_password(user_data.password),
        )
        return self.user_repo.create(user)

    def get_user_by_id(self, user_id: int) -> User:
        user = self.user_repo.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User: {user_id} not found")
        return user

    def get_all_users(self) -> Sequence[User]:
        return self.user_repo.find_all()

    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        user = self.user_repo.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User with id {user_id} not found")
        if self.user_repo.exists_by_email_for_other_user(
            user_data.email,
            user_id,
        ):
            raise DuplicateEmailError(f"Email: {user_data.email} already exists")
        user.name = user_data.name
        user.email = user_data.email
        user.phone = user_data.phone

        return self.user_repo.update(user)

    def delete_user(self, user_id: int) -> None:
        deleted_user = self.user_repo.delete(user_id)
        if not deleted_user:
            raise UserNotFoundError(f"User: {user_id} not found")
