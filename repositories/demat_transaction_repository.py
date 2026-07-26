import logging
from collections.abc import Sequence
from decimal import Decimal

# from typing import Any
from sqlalchemy import exists, select
from sqlalchemy.orm import Session

# from psycopg2.extensions import connection
# from config.database_connection import get_cursor
from models.demat_transaction import DematTransaction

logger = logging.getLogger(__name__)


class DematTransactionRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_id(self, transaction_id: int) -> DematTransaction | None:
        return self.session.get(DematTransaction, transaction_id)

    def find_all_by_holding(self, holding_id: int) -> Sequence[DematTransaction]:
        stmt = select(DematTransaction).where(DematTransaction.holding_id == holding_id)
        transactions = self.session.execute(stmt).scalars().all()
        if not transactions:
            logger.debug("No transactions found for holding: %d", holding_id)
        return transactions

    def find_by_transaction_type(
        self, transaction_type: str
    ) -> Sequence[DematTransaction]:
        stmt = select(DematTransaction).where(
            DematTransaction.transaction_type == transaction_type
        )
        transactions = self.session.execute(stmt).scalars().all()
        if not transactions:
            logger.debug("No transactions with type %s were found", transaction_type)
        return transactions

    def find_recent_transactions(self, limit: int = 5) -> Sequence[DematTransaction]:
        stmt = (
            select(DematTransaction)
            .order_by(DematTransaction.transaction_time.desc())
            .limit(limit)
        )
        transactions = self.session.execute(stmt).scalars().all()
        if not transactions:
            logger.debug("No recent transactions found")
        return transactions

    def exists_by_id(self, transaction_id: int) -> bool | None:
        stmt = select(exists().where(DematTransaction.id == transaction_id))
        return self.session.scalar(stmt)

    def create(self, transaction: DematTransaction) -> DematTransaction:
        self.session.add(transaction)
        self.session.flush()
        logger.info(
            "Transaction with id: %d, holding: %d was created",
            transaction.id,
            transaction.holding_id,
        )
        return transaction

    def update_brokerage(
        self, transaction_id: int, brokerage: Decimal
    ) -> DematTransaction | None:
        transaction = self.session.get(DematTransaction, transaction_id)
        if transaction is None:
            logger.debug("No transaction with id: %d was found", transaction_id)
            return None
        transaction.brokerage = brokerage
        self.session.flush()
        logger.info(
            "Brokerage was updated to %s for transaction id: %d",
            brokerage,
            transaction_id,
        )
        return transaction

    def delete(self, transaction_id: int) -> bool:
        transaction = self.session.get(DematTransaction, transaction_id)
        if transaction is None:
            logger.debug("No transactions with id: %d were found", transaction_id)
            return False
        self.session.delete(transaction)
        self.session.flush()
        logger.info("Transaction with id: %d was deleted", transaction_id)
        return True
