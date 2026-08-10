# Finance Portfolio Tracker

A personal finance management system built in Python for tracking bank accounts, transactions, demat accounts, and investment portfolios.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- psycopg2
- Alembic
- Pydantic
- pytest

## Architecture

The project follows a layered architecture that separates API handling, business logic, and data persistence.

```text
                    FastAPI
                       │
                    Routers
                       │
                Pydantic Schemas
                       │
                    Services
                       │
                  Repositories
                       │
                SQLAlchemy ORM
                       │
                   PostgreSQL
Models

SQLAlchemy 2.0 ORM models using typed Mapped attributes.

Schemas

Pydantic models used for API request validation and response serialization.

Routers

FastAPI routers responsible for handling HTTP requests, dependency injection, and API responses.

Services

Business logic and validation, including custom exception handling and domain-level rules.

Repositories

Data-access layer responsible for database operations. The project contains both raw psycopg2 repositories and SQLAlchemy-based repositories.

Migrations

Alembic is used for database schema versioning and migrations.

Database Schema

The database currently contains 7 tables:

users
bank_accounts
bank_categories
bank_transactions
demat_accounts
demat_holdings
demat_transactions
Database Relationships
User
├── Bank Accounts
│   └── Bank Transactions
│       └── Bank Categories
│
└── Demat Accounts
    └── Demat Holdings
        └── Demat Transactions
API

The application currently exposes FastAPI endpoints for users, bank accounts, and bank transactions.

Users
Method	Endpoint	Description
GET	/users/	Get all users
GET	/users/{user_id}	Get a user by ID
POST	/users/	Create a new user
PUT	/users/{user_id}	Update a user
DELETE	/users/{user_id}	Delete a user
Bank Accounts
Method	Endpoint	Description
POST	/bank_accounts/	Create a bank account
GET	/bank_accounts/{account_id}	Get a bank account by ID
GET	/bank_accounts/users/{user_id}	Get all bank accounts belonging to a user
PUT	/bank_accounts/{account_id}	Update the bank account name
DELETE	/bank_accounts/{account_id}	Delete a bank account
Bank Transactions
Method	Endpoint	Description
POST	/bank_transactions/	Create a bank transaction
GET	/bank_transactions/recent	Get recent transactions
GET	/bank_transactions/{transaction_id}	Get a transaction by ID
GET	/bank_transactions/account/{account_id}	Get transactions for a bank account
GET	/bank_transactions/category/{category_id}	Get transactions by category
Transaction Business Logic

Creating a bank transaction performs validation before persisting the transaction:

Validates that the bank account exists
Validates that the category exists
Validates that the transaction amount is greater than zero
Handles CREDIT transactions by increasing the account balance
Handles DEBIT transactions by decreasing the account balance
Prevents debit transactions when the account has insufficient funds
Updates the bank account balance when the transaction is created
API Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI
http://127.0.0.1:8000/docs
ReDoc
http://127.0.0.1:8000/redoc
Health Check
GET /health

Returns:

{
    "status": "healthy"
}
Project Structure
finance_portfolio_tracker/
│
├── alembic/
├── config/
├── dependencies/
├── exceptions/
├── models/
├── repositories/
├── routers/
├── schemas/
├── service/
├── sql/
├── tests/
│
├── .env
├── alembic.ini
├── create_schema.py
├── main.py
├── main_run.py
├── pyproject.toml
├── README.md
└── requirements.txt
Setup
1. Clone the repository
git clone <repository-url>
cd finance_portfolio_tracker
2. Create a virtual environment
python -m venv .venv

Activate the virtual environment.

Windows:

.venv\Scripts\activate

Linux/macOS:

source .venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables

Create a .env file and provide your PostgreSQL database credentials:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_user
DB_PASS=your_password
5. Run database migrations
alembic upgrade head
6. Start the FastAPI application

For development:

fastapi dev main.py

The API will be available at:

http://127.0.0.1:8000
Testing

Run the test suite using:

pytest
Error Handling

The application uses a custom exception hierarchy in the service layer.

Examples include:

UserNotFoundError
DuplicateEmailError
AccountNotFoundError
CategoryNotFoundError
InsufficientFundsError

These domain-level exceptions are handled by FastAPI exception handlers and mapped to appropriate HTTP responses.

For example:

UserNotFoundError
        ↓
HTTP 404 Not Found
DuplicateEmailError
        ↓
HTTP 409 Conflict
Database Transactions

Database operations use SQLAlchemy sessions with explicit transaction handling.

Successful operations are committed, while exceptions trigger a rollback.

Request
   │
   ▼
Service
   │
   ├── Success ──→ Commit
   │
   └── Exception ──→ Rollback

This is particularly important for bank transactions, where creating a transaction and updating the corresponding bank account balance should occur within the same database transaction.

Project Status
Completed
PostgreSQL database design
SQLAlchemy 2.0 ORM models
Raw psycopg2 repository implementations
SQLAlchemy repository implementations
Service layer
Custom exception hierarchy
FastAPI application setup
FastAPI dependency injection
Pydantic request/response schemas
Global FastAPI exception handlers
Alembic migrations
User API
Bank Account API
Bank Transaction API
Bank transaction balance management
API validation and error handling
In Progress
Demat Account API
Demat Holdings API
Demat Transaction API
Investment portfolio APIs
Portfolio aggregation and analytics
Authentication and authorization
Password hashing
Additional API and integration tests