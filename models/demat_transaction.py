from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.base import Base

if TYPE_CHECKING:
    from models.demat_holding import DematHolding


class TransactionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class DematTransaction(Base):
    __tablename__ = "demat_transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    holding_id: Mapped[int] = mapped_column(
        ForeignKey("demat_holdings.id"), nullable=False
    )
    transaction_type: Mapped[TransactionType] = mapped_column(
        SQLAlchemyEnum(TransactionType), nullable=False
    )
    quantity: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    price_per_unit: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    brokerage: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    transaction_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    demat_holding: Mapped["DematHolding"] = relationship(back_populates="transactions")
