import logging
from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.bank_account import BankAccount

# from psycopg2.extensions import connection
# from config.database_connection import get_cursor
from models.bank_transaction import BankTransaction

logger = logging.getLogger(__name__)


class BankTransactionRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_id(self, transaction_id: int) -> BankTransaction | None:
        return self.session.get(BankTransaction, transaction_id)

    def find_by_account_id(self, account_id: int) -> Sequence[BankTransaction]:
        stmt = select(BankTransaction).where(
            BankTransaction.bank_account_id == account_id
        )
        account = self.session.execute(stmt).scalars().all()
        if not account:
            logger.debug("No transactions frmo account: %d", account_id)
        return account

    def find_by_category_id(self, category_id: int, user_id: int) -> Sequence[BankTransaction]:
        return (
            self.session.query(BankTransaction)
            .join(
                BankAccount,
                BankTransaction.bank_account_id == BankAccount.id,
            )
            .filter(
                BankTransaction.category_id == category_id,
                BankAccount.user_id == user_id,
            )
            .all()
        )

    def find_by_date_range(
        self, from_time: datetime, to_time: datetime
    ) -> Sequence[BankTransaction]:
        stmt = (
            select(BankTransaction)
            .where(BankTransaction.transaction_timestamp.between(from_time, to_time))
            .order_by(BankTransaction.transaction_timestamp)
        )
        transactions = self.session.execute(stmt).scalars().all()
        if not transactions:
            logger.debug("No transactions between %s and %s", from_time, to_time)
        return transactions

    def find_recent_transactions(self, limit: int = 5) -> Sequence[BankTransaction]:
        stmt = (
            select(BankTransaction)
            .order_by(BankTransaction.transaction_timestamp.desc())
            .limit(limit)
        )
        transactions = self.session.execute(stmt).scalars().all()
        if not transactions:
            logger.debug("No transactions done recently")
        return transactions

    def find_by_account_and_date_range(
        self, account_id: int, from_time: datetime, to_time: datetime
    ) -> Sequence[BankTransaction]:
        stmt = select(BankTransaction).where(
            BankTransaction.bank_account_id == account_id,
            BankTransaction.transaction_timestamp.between(from_time, to_time),
        )
        transactions = self.session.execute(stmt).scalars().all()
        if not transactions:
            logger.debug(
                "No transactions found for %d between %s and %s",
                account_id,
                from_time,
                to_time,
            )
        return transactions

    def find_all(self) -> Sequence[BankTransaction]:
        stmt = select(BankTransaction)
        transactions = self.session.execute(stmt).scalars().all()
        if not transactions:
            logger.debug("No transactions found")
        return transactions

    def create(self, transaction_data: BankTransaction) -> BankTransaction:
        self.session.add(transaction_data)
        self.session.flush()
        logger.info("Transaction %d was created", transaction_data.id)
        return transaction_data

    def delete(self, id: int) -> bool:
        transaction = self.session.get(BankTransaction, id)
        if transaction is None:
            logger.debug("Transaction %d was not found", id)
            return False
        self.session.delete(transaction)
        self.session.flush()
        logger.info("Transaction %d was deleted", id)
        return True
