from decimal import Decimal

import pytest

from models.bank_account import BankAccount, Currency
from models.user import User


def test_create_account(account_repo, sample_user):
    account = BankAccount(
                user_id=sample_user.id,
                bank_name="HDFC Bank",
                account_name="Primary Savings",
                account_number="123456789012",
                balance=Decimal("10000.00"),
                currency=Currency.INR,
            )

    created_account = account_repo.create(account)
    assert created_account.id is not None
    saved = account_repo.find_by_id(created_account.id)

    assert saved is not None
    assert saved.user_id == account.user_id
    assert saved.bank_name == account.bank_name
    assert saved.account_name == account.account_name
    assert saved.account_number == account.account_number
    assert saved.balance == account.balance
    assert saved.currency == account.currency
    assert saved.created_at == created_account.created_at

def test_find_by_id(account_repo, sample_bank_account: BankAccount):
    found_account = account_repo.find_by_id(sample_bank_account.id)
    assert found_account is not None
    assert found_account.id == sample_bank_account.id
    assert found_account.bank_name == sample_bank_account.bank_name
    assert found_account.account_name == sample_bank_account.account_name
    assert found_account.account_number == sample_bank_account.account_number
    assert found_account.balance == sample_bank_account.balance
    assert found_account.currency == sample_bank_account.currency
    assert found_account.created_at == sample_bank_account.created_at

def test_find_by_account_number(account_repo, sample_bank_account: BankAccount):
    found_account = account_repo.find_by_account_number(sample_bank_account.account_number)
    assert found_account is not None
    assert found_account.id == sample_bank_account.id
    assert found_account.bank_name == sample_bank_account.bank_name
    assert found_account.account_name == sample_bank_account.account_name
    assert found_account.account_number == sample_bank_account.account_number
    assert found_account.balance == sample_bank_account.balance
    assert found_account.currency == sample_bank_account.currency
    assert found_account.created_at == sample_bank_account.created_at   

def test_find_all_by_user_id(account_repo, sample_user, user_repo):
    user1 = sample_user
    user2 = User(
                name="Bob",
                email="bob@example.com",
                password_hash="password",
            )
    user2 = user_repo.create(user2)

    account1 = BankAccount(
            user_id=user1.id,
            bank_name="HDFC",
            account_name="Savings",
            account_number="111111",
            balance=Decimal("1000"),
            currency=Currency.INR,
        )

    account2 = BankAccount(
        user_id=user1.id,
        bank_name="ICICI",
        account_name="Salary",
        account_number="222222",
        balance=Decimal("5000"),
        currency=Currency.INR,
    )

    account3 = BankAccount(
        user_id=user2.id,
        bank_name="SBI",
        account_name="Savings",
        account_number="333333",
        balance=Decimal("900"),
        currency=Currency.INR,
    )

    account_repo.create(account1)
    account_repo.create(account2)
    account_repo.create(account3)

    accounts = account_repo.find_all_by_user(user1.id)
    accounts2 = account_repo.find_all_by_user(user2.id)

    assert len(accounts) == 2
    assert len(accounts2) == 1
    assert all(account.user_id == user1.id for account in accounts)
    assert all(account.user_id == user2.id for account in accounts2)
    account_numbers = {account.account_number for account in accounts}
    assert account_numbers == {"111111", "222222"}

def test_find_all_by_user_id_returns_empty_list_for_invalid_user(account_repo):
    accounts = account_repo.find_all_by_user(909090)
    assert accounts == []
