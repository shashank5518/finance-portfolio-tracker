import logging
from decimal import Decimal
from typing import Any

from psycopg2.extensions import connection

from config.database_connection import get_cursor
from models.demat_portfolio import Portfolio, PortfolioCreate

logger = logging.getLogger(__name__)


class DematPortfolioRepository:

    def find_by_id(
        self, portfolio_id: int, conn: connection | None = None
    ) -> Portfolio | None:
        with get_cursor(conn) as cur:
            cur.execute("SELECT * FROM dematportfolio WHERE id = %s", (portfolio_id,))
            row = cur.fetchone()
        if not row:
            logger.debug("Portfolio with id = %d not found", portfolio_id)
            return None
        return self._to_demat_portfolio(row)

    def find_all_by_account(
        self, demat_id: int, conn: connection | None = None
    ) -> list[Portfolio]:
        with get_cursor(conn) as cur:
            cur.execute(
                "SELECT * FROM dematportfolio WHERE demat_account_id = %s ORDER BY quantity DESC",
                (demat_id,),
            )
            rows = cur.fetchall()
        return [self._to_demat_portfolio(row) for row in rows]

    def find_by_account_and_ticker(
        self, demat_id: int, ticker: str, conn: connection | None = None
    ) -> Portfolio | None:
        with get_cursor(conn) as cur:
            cur.execute(
                "SELECT * FROM dematportfolio WHERE demat_account_id = %s AND ticker = %s",
                (demat_id, ticker),
            )
            row = cur.fetchone()
        if not row:
            logger.debug(
                "No portfolio found with demat id = %d and ticker = %s",
                demat_id,
                ticker,
            )
            return None
        return self._to_demat_portfolio(row)

    def exists_by_account_and_ticker(
        self, demat_id: int, ticker: str, conn: connection | None = None
    ) -> bool:
        with get_cursor(conn) as cur:
            cur.execute(
                "SELECT 1 FROM dematportfolio WHERE demat_account_id = %s AND ticker = %s",
                (demat_id, ticker),
            )
            return cur.fetchone() is not None

    def create(
        self, portfolio_data: PortfolioCreate, conn: connection | None = None
    ) -> Portfolio:
        with get_cursor(conn) as cur:
            cur.execute(
                "INSERT INTO dematportfolio (demat_account_id, ticker, asset_name, asset_type, quantity, average_buy_price) VALUES(%s, %s, %s, %s, %s, %s) RETURNING *",
                (
                    portfolio_data.demat_account_id,
                    portfolio_data.ticker,
                    portfolio_data.asset_name,
                    portfolio_data.asset_type,
                    portfolio_data.quantity,
                    portfolio_data.average_buy_price,
                ),
            )
            row = cur.fetchone()
        portfolio = self._to_demat_portfolio(row)
        logger.info("Portfolio created : demat_id = %d", portfolio.demat_account_id)
        return portfolio

    def update_position(
        self,
        portfolio_id: int,
        quantity: Decimal,
        average_price: Decimal,
        conn: connection | None = None,
    ) -> Portfolio | None:
        with get_cursor(conn) as cur:
            cur.execute(
                "UPDATE dematportfolio SET quantity = %s, average_buy_price = %s WHERE id = %s RETURNING *",
                (quantity, average_price, portfolio_id),
            )
            row = cur.fetchone()
        if not row:
            logger.debug("Portfolio id = %d not updated", portfolio_id)
            return None
        logger.info("Updated portfolio with id = %d", portfolio_id)
        return self._to_demat_portfolio(row)

    def delete(self, portfolio_id: int, conn: connection | None = None) -> bool:
        with get_cursor(conn) as cur:
            cur.execute(
                "DELETE FROM dematportfolio WHERE id = %s RETURNING *", (portfolio_id,)
            )
            deleted = cur.rowcount > 0
        if not deleted:
            logger.debug("Portfolio with id = %d not deleted", portfolio_id)
        else:
            logger.info("Portfolio id = %d was deleted", portfolio_id)
        return deleted

    @staticmethod
    def _to_demat_portfolio(row: dict[str, Any]) -> Portfolio:
        return Portfolio(**row)
