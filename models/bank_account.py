from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.base import Base

if TYPE_CHECKING:
    from models.bank_transaction import BankTransaction
    from models.user import User


class Currency(str, Enum):
    INR = "INR"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"


class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    bank_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    account_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    account_number: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )
    currency: Mapped[Currency] = mapped_column(
        SQLEnum(Currency),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="bank_accounts",
    )

    transactions: Mapped[list["BankTransaction"]] = relationship(
        back_populates="bank_account",
        cascade="all, delete-orphan",
    )
