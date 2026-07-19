import logging
from typing import Any

from psycopg2.extensions import connection

from config.database_connection import get_cursor
from models.demat_account import DematAccount, DematAccountCreate

logger = logging.getLogger(__name__)


class DematAccountRepository:

    def find_by_id(
        self, account_id: int, conn: connection | None = None
    ) -> DematAccount | None:
        with get_cursor(conn) as cur:
            cur.execute("SELECT * FROM demataccount WHERE id = %s", (account_id,))
            row = cur.fetchone()
        if not row:
            logger.debug("Demat account with id = %d not found", account_id)
            return None
        return self._to_demat_acc(row)

    def find_by_broker_acc_id(
        self, broker_acc_id: str, conn: connection | None = None
    ) -> DematAccount | None:
        with get_cursor(conn) as cur:
            cur.execute(
                "SELECT * FROM demataccount WHERE broker_account_id = %s",
                (broker_acc_id,),
            )
            row = cur.fetchone()
        if not row:
            logger.debug("Account with broker id = %s not found", broker_acc_id)
            return None
        return self._to_demat_acc(row)

    def find_all_by_user(
        self, user_id: int, conn: connection | None = None
    ) -> list[DematAccount]:
        with get_cursor(conn) as cur:
            cur.execute(
                "SELECT * FROM demataccount WHERE user_id = %s ORDER BY created_at ASC",
                (user_id,),
            )
            rows = cur.fetchall()
        return [self._to_demat_acc(row) for row in rows]

    def exists_by_broker_account_id(
        self, broker_acc_id: str, conn: connection | None = None
    ) -> bool:
        with get_cursor(conn) as cur:
            cur.execute(
                "SELECT 1 FROM demataccount WHERE broker_account_id = %s",
                (broker_acc_id,),
            )
            return cur.fetchone() is not None

    def create(
        self, demat_acc_data: DematAccountCreate, conn: connection | None = None
    ) -> DematAccount:
        with get_cursor(conn) as cur:
            cur.execute(
                "INSERT INTO demataccount (user_id, broker_name, account_name, broker_account_id) VALUES (%s, %s, %s, %s) RETURNING *",
                (
                    demat_acc_data.user_id,
                    demat_acc_data.broker_name,
                    demat_acc_data.account_name,
                    demat_acc_data.broker_account_id,
                ),
            )
            row = cur.fetchone()
        demat_account = self._to_demat_acc(row)
        logger.info("Demat Account Created: account_id = %d", demat_account.id)
        return demat_account

    def update_account_name(
        self, account_id: int, account_name: str, conn: connection | None = None
    ) -> DematAccount | None:
        with get_cursor(conn) as cur:
            cur.execute(
                "UPDATE demataccount SET account_name = %s WHERE id = %s RETURNING *",
                (account_name, account_id),
            )
            row = cur.fetchone()
        if not row:
            logger.debug("Update failed - id = %d not found", account_id)
            return None
        updated_demat_acc_data = self._to_demat_acc(row)
        logger.info(
            "Updated account name to %s, id = %d",
            updated_demat_acc_data.account_name,
            updated_demat_acc_data.id,
        )
        return updated_demat_acc_data

    def delete(self, account_id: int, conn: connection | None = None) -> bool:
        with get_cursor(conn) as cur:
            cur.execute(
                "DELETE FROM demataccount WHERE id = %s RETURNING *", (account_id,)
            )
            deleted = cur.rowcount > 0
        if deleted:
            logger.info("Demat Account with id = %d deleted", account_id)
        else:
            logger.debug("Demat account with id = %d not found", account_id)
        return deleted

    @staticmethod
    def _to_demat_acc(row: dict[str, Any]) -> DematAccount:
        return DematAccount(**row)
