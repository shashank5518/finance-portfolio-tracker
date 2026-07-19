from exceptions.bank_account_exceptions import (
    AccountNotFoundError,
    DuplicateAccountNumberError,
)
from exceptions.user_service_exceptions import (
    DeletionFailedError,
    UpdateFailedError,
    UserNotFoundError,
)
from repositories.bank_account_repository import (
    BankAccount,
    BankAccountCreate,
    BankAccountRepository,
)
from repositories.user_repository import UserRepository


class BankAccountService:

    def __init__(
        self, user_repo: UserRepository, bank_repo: BankAccountRepository
    ) -> None:
        self.user_repo = user_repo
        self.bank_repo = bank_repo

    def create_account(self, account_data: BankAccountCreate) -> BankAccount:
        user = self.user_repo.find_by_id(account_data.user_id)
        if user is None:
            raise UserNotFoundError(f"User '{account_data.user_id}' not found.")
        if self.bank_repo.exists_by_account_number(account_data.account_number):
            raise DuplicateAccountNumberError(
                f"Account '{account_data.account_number}' already exists."
            )
        return self.bank_repo.create(account_data)

    def get_account_by_id(self, account_id: int) -> BankAccount:
        account = self.bank_repo.find_by_id(account_id)
        if account is None:
            raise AccountNotFoundError(f"Account {account_id} does not exist.")
        return account

    def get_accounts_by_user(self, user_id: int) -> list[BankAccount]:
        user = self.user_repo.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User '{user_id}' not found.")
        accounts = self.bank_repo.find_all_by_user(user_id)
        return accounts

    def update_account_name(self, account_id: int, new_name: str) -> BankAccount:
        self.get_account_by_id(account_id)
        new_name_account = self.bank_repo.update_account_name(account_id, new_name)
        if new_name_account is None:
            raise UpdateFailedError(f"Account '{account_id}' was not updated.")
        return new_name_account

    def delete_account(self, account_id: int) -> None:
        self.get_account_by_id(account_id)
        if not self.bank_repo.delete_account(account_id):
            raise DeletionFailedError(f"Delete on '{account_id}' failed.")
