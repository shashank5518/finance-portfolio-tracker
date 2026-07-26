import logging

# from typing import Any
from collections.abc import Sequence
from decimal import Decimal

from sqlalchemy import exists, select
from sqlalchemy.orm import Session

# from psycopg2.extensions import connection
# from config.database_connection import get_cursor
from models.demat_holding import DematHolding

logger = logging.getLogger(__name__)


class DematHoldingRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_id(self, holding_id: int) -> DematHolding | None:
        return self.session.get(DematHolding, holding_id)

    def find_all_by_account(self, demat_id: int) -> Sequence[DematHolding]:
        stmt = select(DematHolding).where(DematHolding.demat_account_id == demat_id)
        holdings = self.session.execute(stmt).scalars().all()
        if not holdings:
            logger.debug("No holdings for demat account id: %d were found", demat_id)
        return holdings

    def find_by_account_and_ticker(
        self, demat_id: int, ticker: str
    ) -> DematHolding | None:
        stmt = select(DematHolding).where(
            DematHolding.demat_account_id == demat_id, DematHolding.ticker == ticker
        )
        holding = self.session.execute(stmt).scalar_one_or_none()
        if holding is None:
            logger.debug(
                "No holdings for demat id: %d and ticker: %s were found",
                demat_id,
                ticker,
            )
        return holding

    def exists_by_account_and_ticker(self, demat_id: int, ticker: str) -> bool | None:
        stmt = select(
            exists().where(
                DematHolding.demat_account_id == demat_id, DematHolding.ticker == ticker
            )
        )
        return self.session.scalar(stmt)

    def create(self, holding_data: DematHolding) -> DematHolding:
        self.session.add(holding_data)
        self.session.flush()
        logger.info(
            "Holding with id: %d and ticker: %s was inserted",
            holding_data.id,
            holding_data.ticker,
        )
        return holding_data

    def update_position(
        self,
        holding_id: int,
        quantity: Decimal,
        average_price: Decimal,
    ) -> DematHolding | None:
        holding = self.session.get(DematHolding, holding_id)
        if holding is None:
            logger.debug("No holding with id: %d was found", holding_id)
            return None
        holding.quantity = quantity
        holding.average_buy_price = average_price
        self.session.flush()
        logger.info(
            "Holding was updated to quantity: %s and average buy price: %s",
            quantity,
            average_price,
        )
        return holding

    def delete(self, holding_id: int) -> bool:
        holding = self.session.get(DematHolding, holding_id)
        if holding is None:
            logger.debug("No holding with id: %d was found", holding_id)
            return False
        self.session.delete(holding)
        self.session.flush()
        logger.info("Holding with id: %d was deleted", holding_id)
        return True
