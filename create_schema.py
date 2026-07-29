from config.base import Base
from config.database_connection import engine
from models.bank_account import BankAccount
from models.bank_category import BankCategory
from models.bank_transaction import BankTransaction
from models.budget import Budget
from models.demat_account import DematAccount
from models.demat_holding import DematHolding
from models.demat_transaction import DematTransaction
from models.user import User


def create_schema() -> None:
    Base.metadata.create_all(bind=engine)
    print("Database schema created successfully.")


if __name__ == "__main__":
    create_schema()
