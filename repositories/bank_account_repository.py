import logging
from decimal import Decimal
from typing import Any

from psycopg2.extensions import connection

from config.database_connection import get_cursor
from models.bank_account import BankAccount, BankAccountCreate

logger = logging.getLogger(__name__)


class BankAccountRepository:

    def find_by_account_number(
        self, account_number: str, conn: connection | None = None
    ) -> BankAccount | None:
        with get_cursor(conn) as cur:
            cur.execute(
                "SELECT * FROM bankaccount WHERE account_number = %s", (account_number,)
            )
            row = cur.fetchone()
        if not row:
            logger.debug("Account Number: %s Not Found", account_number)
            return None
        return self._to_bank(row)

    def find_by_id(
        self, account_id: int, conn: connection | None = None
    ) -> BankAccount | None:
        with get_cursor(conn) as cur:
            cur.execute("SELECT * FROM bankaccount WHERE id = %s", (account_id,))
            row = cur.fetchone()
        if not row:
            logger.debug("Account ID = %d does not exist", account_id)
            return None
        return self._to_bank(row)

    def find_all_by_user(
        self, user_id: int, conn: connection | None = None
    ) -> list[BankAccount]:
        with get_cursor(conn) as cur:
            cur.execute(
                "SELECT * FROM bankaccount WHERE user_id = %s ORDER BY created_at DESC",
                (user_id,),
            )
            rows = cur.fetchall()
        return [self._to_bank(row) for row in rows]

    def create(
        self, account_data: BankAccountCreate, conn: connection | None = None
    ) -> BankAccount:
        with get_cursor(conn) as cur:
            cur.execute(
                "INSERT INTO bankaccount(user_id, bank_name, account_name, account_number, balance, currency) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *",
                (
                    account_data.user_id,
                    account_data.bank_name,
                    account_data.account_name,
                    account_data.account_number,
                    account_data.balance,
                    account_data.currency,
                ),
            )
            row = cur.fetchone()
        account = self._to_bank(row)
        logger.info("Account created: number = %s", account.account_number)
        return account

    def update_balance(
        self, account_number: str, new_balance: Decimal, conn: connection | None = None
    ) -> BankAccount | None:
        with get_cursor(conn) as cur:
            cur.execute(
                "UPDATE bankaccount SET balance = %s WHERE account_number = %s RETURNING *",
                (new_balance, account_number),
            )
            row = cur.fetchone()
        if not row:
            logger.debug(
                "Update failed - Account not found: account_number = %s", account_number
            )
            return None
        account = self._to_bank(row)
        logger.info(
            "Balance Updated: balance: %s, account_number: %s",
            account.balance,
            account.account_number,
        )
        return account

    def update_account_name(
        self, account_id: int, new_name: str, conn: connection | None = None
    ) -> BankAccount | None:
        with get_cursor(conn) as cur:
            cur.execute(
                "UPDATE bankaccount SET account_name = %s WHERE id = %s",
                (new_name, account_id),
            )
            row = cur.fetchone()
        if not row:
            logger.debug("Update failed, for id = %d", account_id)
            return None
        return self._to_bank(row)

    def delete_account(self, account_id: int, conn: connection | None = None) -> bool:
        with get_cursor(conn) as cur:
            cur.execute("DELETE FROM bankaccount WHERE account_id = %s", (account_id,))
            deleted = cur.rowcount > 0
        logger.info("Account deleted: acc_id = %s", account_id)
        return deleted

    def exists_by_account_number(
        self, account_number: str, conn: connection | None = None
    ) -> bool:
        with get_cursor(conn) as cur:
            cur.execute(
                "SELECT 1 FROM bankaccount WHERE account_number = %s", (account_number,)
            )
            return cur.fetchone() is not None

    @staticmethod
    def _to_bank(row: dict[str, Any]) -> BankAccount:
        return BankAccount(**row)
