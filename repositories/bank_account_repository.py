import logging
from collections.abc import Sequence
from decimal import Decimal

from sqlalchemy import exists, select

# from typing import Any
from sqlalchemy.orm import Session

# from psycopg2.extensions import connection
# from config.database_connection import get_cursor
from models.bank_account import BankAccount

logger = logging.getLogger(__name__)


class BankAccountRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_account_number(self, account_number: str) -> BankAccount | None:
        stmt = select(BankAccount).where(BankAccount.account_number == account_number)
        return self.session.execute(stmt).scalar_one_or_none()

    def find_by_id(self, account_id: int) -> BankAccount | None:
        return self.session.get(BankAccount, account_id)

    def find_all_by_user(self, user_id: int) -> Sequence[BankAccount]:
        stmt = select(BankAccount).where(BankAccount.user_id == user_id)
        return self.session.execute(stmt).scalars().all()

    def create(self, bank_account: BankAccount) -> BankAccount:
        self.session.add(bank_account)
        self.session.flush()

        logger.info(
            "Bank account created: id = %d, account_number = %s",
            bank_account.id,
            bank_account.account_number,
        )
        return bank_account

    def update_balance(
        self, account_number: str, new_balance: Decimal
    ) -> BankAccount | None:
        stmt = select(BankAccount).where(BankAccount.account_number == account_number)
        account = self.session.execute(stmt).scalar_one_or_none()
        if account is None:
            logger.debug("Account number : %s does not exist", account_number)
            return None
        account.balance = new_balance
        self.session.flush()
        logger.info("Balance was updated for account : %s", account_number)
        return account

    def update_account_name(self, account_id: int, new_name: str) -> BankAccount | None:
        account = self.session.get(BankAccount, account_id)
        if account is None:
            logger.debug("Account id: %d does not exist", account_id)
            return None
        account.account_name = new_name
        self.session.flush()
        logger.info("Updated account : %d and name : %s", account_id, new_name)
        return account

    def delete_account(self, account_id: int) -> bool:
        account = self.session.get(BankAccount, account_id)
        if account is None:
            logger.debug("Account : %d was not found", account_id)
            return False
        self.session.delete(account)
        self.session.flush()
        logger.info("Deleted account : %d", account_id)
        return True

    def exists_by_account_number(self, account_number: str) -> bool | None:
        stmt = select(exists().where(BankAccount.account_number == account_number))
        return self.session.scalar(stmt)
