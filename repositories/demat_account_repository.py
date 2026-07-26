import logging
from collections.abc import Sequence

from sqlalchemy import exists, select
from sqlalchemy.orm import Session

# from psycopg2.extensions import connection
# from config.database_connection import get_cursor
from models.demat_account import DematAccount

logger = logging.getLogger(__name__)


class DematAccountRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_id(self, account_id: int) -> DematAccount | None:
        return self.session.get(DematAccount, account_id)

    def find_by_broker_acc_id(self, broker_acc_id: str) -> DematAccount | None:
        stmt = select(DematAccount).where(
            DematAccount.broker_account_id == broker_acc_id
        )
        demat_account = self.session.execute(stmt).scalar_one_or_none()
        if demat_account is None:
            logger.debug(
                "No demat account with broker acocunt: %s found", broker_acc_id
            )
            return None
        return demat_account

    def find_all_by_user(self, user_id: int) -> Sequence[DematAccount]:
        stmt = select(DematAccount).where(DematAccount.user_id == user_id)
        demat_account = self.session.execute(stmt).scalars().all()
        if not demat_account:
            logger.debug("No demat accounts associated with user %d found", user_id)
        return demat_account

    def exists_by_broker_account_id(self, broker_acc_id: str) -> bool | None:
        stmt = select(exists().where(DematAccount.broker_account_id == broker_acc_id))
        return self.session.scalar(stmt)

    def create(self, demat_acc_data: DematAccount) -> DematAccount:
        self.session.add(demat_acc_data)
        self.session.flush()
        logger.info("Demat account %d was created", demat_acc_data.id)
        return demat_acc_data

    def update_account_name(
        self, account_id: int, account_name: str
    ) -> DematAccount | None:
        demat_account = self.session.get(DematAccount, account_id)
        if demat_account is None:
            logger.debug("No demat account with id: %d was found", account_id)
            return None
        demat_account.account_name = account_name
        self.session.flush()
        logger.info("Account name was updated to %s", account_name)
        return demat_account

    def delete(self, account_id: int) -> bool:
        demat_account = self.session.get(DematAccount, account_id)
        if demat_account is None:
            logger.debug("No account with id: %d was found", account_id)
            return False
        self.session.delete(demat_account)
        self.session.flush()
        logger.info("Demat account with id: %d was deleted", account_id)
        return True
