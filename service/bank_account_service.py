from collections.abc import Sequence

from exceptions.bank_account_exceptions import (
    AccountNotFoundError,
    DuplicateAccountNumberError,
)
from exceptions.user_service_exceptions import (
    UserNotFoundError,
)
from repositories.bank_account_repository import (
    BankAccount,
    BankAccountRepository,
)
from repositories.user_repository import UserRepository
from schemas.bank_account import BankAccountCreate


class BankAccountService:

    def __init__(
        self, user_repo: UserRepository, bank_repo: BankAccountRepository
    ) -> None:
        self.user_repo = user_repo
        self.bank_repo = bank_repo

    def create_account(self, account_data: BankAccountCreate) -> BankAccount:
        user = self.user_repo.find_by_id(account_data.user_id)
        if user is None:
            raise UserNotFoundError(f"User '{account_data.user_id}' not found")
        if self.bank_repo.exists_by_account_number(account_data.account_number):
            raise DuplicateAccountNumberError(
                f"Account Number '{account_data.account_number}' already exists"
            )
        bank_account = BankAccount(
            user_id = account_data.user_id,
            bank_name = account_data.bank_name,
            account_name = account_data.account_name,
            account_number = account_data.account_number,
            balance = account_data.balance,
            currency = account_data.currency
        )
        return self.bank_repo.create(bank_account)

    def get_account_by_id(self, account_id: int) -> BankAccount:
        account = self.bank_repo.find_by_id(account_id)
        if account is None:
            raise AccountNotFoundError(f"Account '{account_id}' not found")
        return account

    def get_accounts_by_user(self, user_id: int) -> Sequence[BankAccount]:
        user = self.user_repo.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User '{user_id}' not found")
        return self.bank_repo.find_all_by_user(user_id)

    def update_account_name(self, account_id: int, new_name) -> BankAccount:
        updated_account = self.bank_repo.update_account_name(account_id, new_name)
        if updated_account is None:
            raise AccountNotFoundError(f"Account '{account_id}' not found")
        return updated_account

    def delete_account(self, account_id: int) -> bool:
        deleted_account = self.bank_repo.delete_account(account_id)
        if not deleted_account:
            raise AccountNotFoundError(f"Account '{account_id}' not found")
        return deleted_account
