import logging
from datetime import datetime
from typing import Any

from psycopg2.extensions import connection

from config.database_connection import get_cursor
from models.bank_transaction import BankTransaction, BankTransactionCreate

logger = logging.getLogger(__name__)


class BankTransactionRepository:

    def find_by_id(
        self, id: int, conn: connection | None = None
    ) -> BankTransaction | None:
        with get_cursor(conn) as cur:
            cur.execute("SELECT * FROM banktransaction WHERE id = %s", (id,))
            row = cur.fetchone()
        if not row:
            logger.debug("Transaction with id = %d not found", id)
            return None
        return self._to_transaction(row)

    def find_by_account_id(
        self, account_id: int, conn: connection | None = None
    ) -> list[BankTransaction]:
        with get_cursor(conn) as cur:
            cur.execute(
                "SELECT * FROM banktransaction WHERE bank_account_id = %s ORDER BY transaction_timestamp DESC",
                (account_id,),
            )
            rows = cur.fetchall()
        return [self._to_transaction(row) for row in rows]

    def find_by_category_id(
        self, category_id: int, conn: connection | None = None
    ) -> list[BankTransaction]:
        with get_cursor(conn) as cur:
            cur.execute(
                "SELECT * FROM banktransaction WHERE category_id = %s ORDER BY transaction_timestamp DESC",
                (category_id,),
            )
            rows = cur.fetchall()
        return [self._to_transaction(row) for row in rows]

    def find_by_date_range(
        self, from_time: datetime, to_time: datetime, conn: connection | None = None
    ) -> list[BankTransaction]:
        with get_cursor(conn) as cur:
            cur.execute(
                "SELECT * FROM banktransaction WHERE transaction_timestamp BETWEEN %s AND %s ORDER BY transaction_timestamp DESC",
                (from_time, to_time),
            )
            rows = cur.fetchall()
        return [self._to_transaction(row) for row in rows]

    def find_recent_transactions(
        self, limit: int = 5, conn: connection | None = None
    ) -> list[BankTransaction]:
        with get_cursor(conn) as cur:
            cur.execute(
                "SELECT * FROM banktransaction ORDER BY transaction_timestamp DESC LIMIT %s",
                (limit,),
            )
            rows = cur.fetchall()
        return [self._to_transaction(row) for row in rows]

    def create(
        self, transaction_data: BankTransactionCreate, conn: connection | None = None
    ) -> BankTransaction:
        with get_cursor(conn) as cur:
            cur.execute(
                "INSERT INTO banktransaction (amount, bank_account_id, transaction_type, description, category_id) VALUES (%s, %s, %s, %s, %s) RETURNING *",
                (
                    transaction_data.amount,
                    transaction_data.bank_account_id,
                    transaction_data.transaction_type,
                    transaction_data.description,
                    transaction_data.category_id,
                ),
            )
            row = cur.fetchone()
        transaction = self._to_transaction(row)
        logger.info("Transaction created: id = %d", transaction.id)
        return transaction

    def delete(self, id: int, conn: connection | None = None) -> BankTransaction | None:
        with get_cursor(conn) as cur:
            cur.execute("DELETE FROM banktransaction WHERE id = %s RETURNING *", (id,))
            row = cur.fetchone()
        if not row:
            logger.debug("Transaction id = %d not found", id)
            return None
        logger.info("Deleted transaction with id = %d", id)
        return self._to_transaction(row)

    @staticmethod
    def _to_transaction(row: dict[str, Any]) -> BankTransaction:
        return BankTransaction(**row)
