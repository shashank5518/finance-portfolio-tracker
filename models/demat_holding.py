from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.base import Base

if TYPE_CHECKING:
    from models.demat_account import DematAccount
    from models.demat_transaction import DematTransaction


class DematHolding(Base):
    __tablename__ = "demat_holdings"

    id: Mapped[int] = mapped_column(primary_key=True)
    demat_account_id: Mapped[int] = mapped_column(
        ForeignKey("demat_accounts.id"), nullable=False
    )
    ticker: Mapped[str] = mapped_column(String(10), nullable=False)
    asset_name: Mapped[str] = mapped_column(String(100), nullable=False)
    asset_type: Mapped[str] = mapped_column(String(25), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    average_buy_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    demat_account: Mapped["DematAccount"] = relationship(back_populates="holdings")
    transactions: Mapped[list["DematTransaction"]] = relationship(
        back_populates="demat_holding", cascade="all, delete-orphan"
    )
