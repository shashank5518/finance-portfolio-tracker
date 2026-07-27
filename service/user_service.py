from collections.abc import Sequence

from exceptions.user_service_exceptions import (
    DuplicateEmailError,
    UserNotFoundError,
)
from repositories.user_repository import User, UserRepository


class UserService:

    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    def create_user(self, user_data: User) -> User:
        if self.user_repo.exists_by_email(user_data.email):
            raise DuplicateEmailError(f"Email: {user_data.email} already exists")
        return self.user_repo.create(user_data)

    def get_user_by_id(self, user_id: int) -> User:
        user = self.user_repo.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User: {user_id} not found")
        return user

    def get_all_users(self) -> Sequence[User]:
        return self.user_repo.find_all()

    def update_user(self, user_id: int, new_name: str) -> User:
        updated_user = self.user_repo.update_name(user_id, new_name)
        if updated_user is None:
            raise UserNotFoundError(f"User: {user_id} not found")
        return updated_user

    def delete_user(self, user_id: int) -> None:
        deleted_user = self.user_repo.delete(user_id)
        if not deleted_user:
            raise UserNotFoundError(f"User: {user_id} not found")
