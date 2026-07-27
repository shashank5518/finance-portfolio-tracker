from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.base import Base
from models.bank_account import BankAccount, Currency
from models.bank_category import BankCategory
from models.bank_transaction import BankTransaction, TransactionType
from models.demat_account import DematAccount
from models.demat_holding import DematHolding
from models.demat_transaction import DematTransaction, TransactionType
from models.user import User
from repositories.bank_account_repository import BankAccountRepository
from repositories.bank_category_repository import BankCategoryRepository
from repositories.bank_transaction_repository import BankTransactionRepository
from repositories.demat_account_repository import DematAccountRepository
from repositories.demat_portfolio_repository import DematHoldingRepository
from repositories.demat_transaction_repository import DematTransactionRepository
from repositories.user_repository import UserRepository
from service.bank_account_service import BankAccountService
from service.bank_transaction_service import BankTransactionService
from service.demat_account_service import DematAccountService
from service.demat_transaction_service import DematTransactionService
from service.user_service import UserService

TEST_DATABASE_URL = ("postgresql+psycopg2://postgres:root@localhost/finance_portfolio_test")

@pytest.fixture(scope = "session")
def engine():
    engine = create_engine(TEST_DATABASE_URL)

    Base.metadata.create_all(engine)

    yield engine

    Base.metadata.drop_all(engine)

@pytest.fixture(scope = "session")
def session_factory(engine):
    return sessionmaker(
        bind = engine, 
        expire_on_commit=False,
    )

@pytest.fixture
def db_session(session_factory):
    session = session_factory()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture
def user_repo(db_session):
    return UserRepository(db_session)

@pytest.fixture
def account_repo(db_session):
    return BankAccountRepository(db_session)

@pytest.fixture
def category_repo(db_session):
    return BankCategoryRepository(db_session)

@pytest.fixture
def transaction_repo(db_session):
    return BankTransactionRepository(db_session)

@pytest.fixture
def demat_account_repo(db_session):
    return DematAccountRepository(db_session)

@pytest.fixture
def demat_holding_repo(db_session):
    return DematHoldingRepository(db_session)

@pytest.fixture
def demat_transaction_repo(db_session):
    return DematTransactionRepository(db_session)

@pytest.fixture
def user_service(user_repo):
    return UserService(user_repo)

@pytest.fixture
def bank_account_service(user_repo, account_repo):
    return BankAccountService(account_repo, user_repo,)

@pytest.fixture
def bank_transaction_service(account_repo, transaction_repo, category_repo):
    return BankTransactionService(account_repo, transaction_repo, category_repo)

@pytest.fixture
def demat_account_service(demat_account_repo, user_repo):
    return DematAccountService(demat_account_repo, user_repo)

@pytest.fixture
def demat_transaction_service(demat_transaction_repo, demat_holding_repo):
    return DematTransactionService(demat_transaction_repo, demat_holding_repo)

@pytest.fixture
def sample_user(user_repo):
    return user_repo.create(
        User(
            name="John Doe",
            email="john@example.com",
            password_hash="hashed_password",
        )
    )

@pytest.fixture
def sample_bank_account(account_repo, sample_user):
    return account_repo.create(
        BankAccount(
            user_id=sample_user.id,
            bank_name="HDFC Bank",
            account_name="Primary Savings",
            account_number="123456789012",
            balance=Decimal("10000.00"),
            currency=Currency.INR,
        )
    )

@pytest.fixture
def sample_category(category_repo):
    return category_repo.create(
        BankCategory(
            name="Salary",
            description="Monthly salary credit",
        )
    )

@pytest.fixture
def sample_bank_transaction(
    transaction_repo,
    sample_bank_account,
    sample_category,
):
    return transaction_repo.create(
        BankTransaction(
            amount=Decimal("5000.00"),
            description="July Salary",
            bank_account_id=sample_bank_account.id,
            transaction_type=TransactionType.CREDIT,
            category_id=sample_category.id,
        )
    )

@pytest.fixture
def sample_demat_account(
    demat_account_repo,
    sample_user,
):
    return demat_account_repo.create(
        DematAccount(
            user_id=sample_user.id,
            broker_name="Zerodha",
            account_name="Long Term Portfolio",
            broker_account_id="ZDH001",
        )
    )

@pytest.fixture
def sample_holding(
    demat_holding_repo,
    sample_demat_account,
):
    return demat_holding_repo.create(
        DematHolding(
            demat_account_id=sample_demat_account.id,
            ticker="TCS",
            asset_name="Tata Consultancy Services",
            asset_type="Stock",
            quantity=Decimal("10.00"),
            average_buy_price=Decimal("3500.00"),
        )
    )

@pytest.fixture
def sample_demat_transaction(
    demat_transaction_repo,
    sample_holding,
):
    return demat_transaction_repo.create(
        DematTransaction(
            holding_id=sample_holding.id,
            transaction_type=TransactionType.BUY,
            quantity=Decimal("5.00"),
            price_per_unit=Decimal("3600.00"),
            brokerage=Decimal("20.00"),
        )
    )