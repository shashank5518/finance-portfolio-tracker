import logging
from decimal import Decimal
from typing import Any

from psycopg2.extensions import connection

from config.database_connection import get_cursor
from models.demat_transaction import InvestmentTransaction, InvestmentTransactionCreate

logger = logging.getLogger(__name__)


class DematTransactionRepository:

    def find_by_id(
        self, transaction_id: int, conn: connection | None = None
    ) -> InvestmentTransaction | None:
        with get_cursor(conn) as cur:
            cur.execute(
                "SELECT * FROM demattransaction WHERE id = %s", (transaction_id,)
            )
            row = cur.fetchone()
        if not row:
            logger.debug("Transaction id = %d not found", transaction_id)
            return None
        return self._to_demat_transaction(row)

    def find_all_by_portfolio(
        self, portfolio_id: int, conn: connection | None = None
    ) -> list[InvestmentTransaction]:
        with get_cursor(conn) as cur:
            cur.execute(
                "SELECT * FROM demattransaction WHERE portfolio_id = %s ORDER BY transaction_time DESC",
                (portfolio_id,),
            )
            rows = cur.fetchall()
        return [self._to_demat_transaction(row) for row in rows]

    def find_by_transaction_type(
        self, transaction_type: str, conn: connection | None = None
    ) -> list[InvestmentTransaction]:
        with get_cursor(conn) as cur:
            cur.execute(
                "SELECT * FROM demattransaction WHERE transaction_type = %s",
                (transaction_type,),
            )
            rows = cur.fetchall()
        return [self._to_demat_transaction(row) for row in rows]

    def find_recent_transactions(
        self, limit: int = 5, conn: connection | None = None
    ) -> list[InvestmentTransaction]:
        with get_cursor(conn) as cur:
            cur.execute(
                "SELECT * FROM demattransaction ORDER BY transaction_time DESC LIMIT %s",
                (limit,),
            )
            rows = cur.fetchall()
        return [self._to_demat_transaction(row) for row in rows]

    def exists_by_id(self, transaction_id: int, conn: connection | None = None) -> bool:
        with get_cursor(conn) as cur:
            cur.execute(
                "SELECT 1 FROM demattransaction WHERE id = %s", (transaction_id,)
            )
            return cur.fetchone() is not None

    def create(
        self, transaction: InvestmentTransactionCreate, conn: connection | None = None
    ) -> InvestmentTransaction:
        with get_cursor(conn) as cur:
            cur.execute(
                "INSERT INTO demattransaction (portfolio_id, transaction_type, quantity, price_per_unit, brokerage) VALUES (%s, %s, %s, %s, %s) RETURNING *",
                (
                    transaction.portfolio_id,
                    transaction.transaction_type,
                    transaction.quantity,
                    transaction.price_per_unit,
                    transaction.brokerage,
                ),
            )
            row = cur.fetchone()
        transaction_data = self._to_demat_transaction(row)
        logger.info("Transaction created, id = %d", transaction_data.id)
        return transaction_data

    def update_brokerage(
        self, transaction_id: int, brokerage: Decimal, conn: connection | None = None
    ) -> InvestmentTransaction | None:
        with get_cursor(conn) as cur:
            cur.execute(
                "UPDATE demattransaction SET brokerage = %s WHERE id = %s RETURNING *",
                (brokerage, transaction_id),
            )
            row = cur.fetchone()
        if not row:
            logger.debug("Update failed for id = %d", transaction_id)
            return None
        logger.info("Brokerage updated")
        return self._to_demat_transaction(row)

    def delete(self, transaction_id: int, conn: connection | None = None) -> bool:
        with get_cursor(conn) as cur:
            cur.execute(
                "DELETE FROM demattransaction WHERE id = %s RETURNING *",
                (transaction_id,),
            )
            deleted = cur.rowcount > 0
        if not deleted:
            logger.debug("Delete failed for id = %d", transaction_id)
        else:
            logger.info("Deleted transaction for id = %d", transaction_id)
        return deleted

    @staticmethod
    def _to_demat_transaction(row: dict[str, Any]) -> InvestmentTransaction:
        return InvestmentTransaction(**row)
