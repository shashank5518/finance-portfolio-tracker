from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.base import Base

if TYPE_CHECKING:
    from finance_portfolio_tracker.models.demat_holding import DematHolding
    from models.user import User


class DematAccount(Base):
    __tablename__ = "demat_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    broker_name: Mapped[str] = mapped_column(String(30), nullable=False)
    account_name: Mapped[str] = mapped_column(String(100), nullable=False)
    broker_account_id: Mapped[str] = mapped_column(
        String(15), unique=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="demat_accounts")
    holdings: Mapped[list["DematHolding"]] = relationship(
        back_populates="demat_account",
        cascade="all, delete-orphan",
    )
