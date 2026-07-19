import logging
from decimal import Decimal

from config.database_connection import close_pool
from models.bank_account import BankAccountCreate
from models.user import UserCreate
from repositories.bank_account_repository import BankAccountRepository
from repositories.user_repository import UserRepository

logging.basicConfig(
    filename="app.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def main() -> None:
    # repo = UserRepository()
    repo = BankAccountRepository()

    # user_data = UserCreate(
    #     name = "Shashank Garg",
    #     email = "shashankg5518@gmail.com",
    #     password_hash = "xxx@yyy1234"
    # )

    # if repo.exists_by_email(user_data.email):
    #     print(f"Email already registered: {user_data.email}")
    # else:
    #     shashank = repo.create(user_data)
    #     print(f"Created: {shashank}")

    # user = repo.find_by_id(1)
    # print(f"Found by ID: {user}")

    # user = repo.find_by_email("shashankg5518@gmail.com")
    # print(f"Found by email: {user}")

    # all_users = repo.find_all()
    # print(f"Total users: {len(all_users)}")

    # updated = repo.update_name(1, "Shashank")
    # print(f"Updated: {updated}")

    # deleted = repo.delete(1)
    # print(f"Deleted: {deleted}")

    account_data = BankAccountCreate(
        user_id=2,
        bank_name="HDFC",
        account_name="Savings",
        account_number="3060408363",
        balance=Decimal(35000),
        currency="INR",
    )

    if repo.exists_by_account_number(account_data.account_number):
        print(
            f"Account with account number = {account_data.account_number} already exists"
        )
    else:
        shashank = repo.create(account_data)
        print(f"Created: {shashank}")


if __name__ == "__main__":
    try:
        main()
    finally:
        close_pool()
