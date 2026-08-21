# Finance Portfolio Tracker

A production-style backend API for managing personal finances and investment portfolios. Built with **FastAPI**, **SQLAlchemy 2.0**, and **PostgreSQL**, the application allows users to securely manage bank accounts, demat accounts, transactions, and investment holdings with JWT authentication and layered architecture.

---

## Features

- User registration and authentication
- Password hashing using bcrypt
- JWT-based authentication and authorization
- Bank account management
- Bank transaction management
- Demat account management
- Demat transaction management
- Investment holdings tracking
- Role-based resource authorization (users can only access their own data)
- Custom exception hierarchy
- Dependency Injection
- SQLAlchemy 2.0 ORM
- Alembic database migrations
- Interactive Swagger API documentation

---

## Tech Stack

- Python 3.13
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- Alembic
- bcrypt
- PyJWT
- python-dotenv
- pytest
- Ruff
- Black
- MyPy

---

## Architecture

The project follows a layered architecture.

```
Client
   │
   ▼
Routers (FastAPI)
   │
   ▼
Services (Business Logic)
   │
   ▼
Repositories (Database Access)
   │
   ▼
PostgreSQL
```

### Project Structure

```
finance_portfolio_tracker/
│
├── routers/
├── service/
├── repositories/
├── models/
├── schemas/
├── dependencies/
├── exceptions/
├── utils/
├── config/
├── migrations/
├── tests/
├── main.py
└── requirements.txt
```

---

## Database Schema

The application consists of the following tables:

- users
- bank_accounts
- bank_categories
- bank_transactions
- demat_accounts
- demat_holdings
- demat_transactions

---

## API Endpoints

### Authentication

| Method | Endpoint |
|---------|----------|
| POST | `/auth/login` |
| GET | `/auth/me` |

---

### Users

| Method | Endpoint |
|---------|----------|
| POST | `/users/` |
| GET | `/users/{user_id}` |
| PUT | `/users/{user_id}` |
| DELETE | `/users/{user_id}` |

---

### Bank Accounts

| Method | Endpoint |
|---------|----------|
| POST | `/bank_accounts/` |
| GET | `/bank_accounts/me` |
| GET | `/bank_accounts/{account_id}` |
| PUT | `/bank_accounts/{account_id}` |
| DELETE | `/bank_accounts/{account_id}` |

---

### Bank Transactions

| Method | Endpoint |
|---------|----------|
| POST | `/bank_transactions/` |
| GET | `/bank_transactions/recent` |
| GET | `/bank_transactions/{transaction_id}` |
| GET | `/bank_transactions/account/{account_id}` |
| GET | `/bank_transactions/category/{category_id}` |

---

### Demat Accounts

| Method | Endpoint |
|---------|----------|
| POST | `/demat_accounts/` |
| GET | `/demat_accounts/me` |
| GET | `/demat_accounts/{account_id}` |
| PUT | `/demat_accounts/{account_id}` |
| DELETE | `/demat_accounts/{account_id}` |

---

### Demat Transactions

| Method | Endpoint |
|---------|----------|
| POST | `/demat_transactions/` |
| GET | `/demat_transactions/{transaction_id}` |
| GET | `/demat_transactions/account/{account_id}` |

---

## Authentication

Authentication is implemented using JWT access tokens.

### Login

```
POST /auth/login
```

Returns

```json
{
    "access_token": "<jwt_token>",
    "token_type": "bearer"
}
```

Authorize requests using

```
Authorization: Bearer <access_token>
```

Protected endpoints require a valid JWT token.

---

## Authorization

Every authenticated user can only access their own resources.

Ownership checks are enforced for:

- Bank Accounts
- Bank Transactions
- Demat Accounts
- Demat Transactions

Attempts to access another user's data return **403 Forbidden**.

---

## Error Handling

The application includes custom exception handling for common business cases.

Examples include:

- UserNotFoundError
- DuplicateEmailError
- DuplicatePhoneError
- AccountNotFoundError
- DuplicateAccountNumberError
- CategoryNotFoundError
- TransactionNotFoundError
- DematAccountNotFoundError
- HoldingNotFoundError
- InsufficientFundsError
- InsufficientSharesError
- InvalidTransactionTypeError
- ForbiddenError

---

## Installation

Clone the repository

```bash
git clone <repository-url>
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name

JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Run migrations

```bash
alembic upgrade head
```

Start the application

```bash
uvicorn main:app --reload
```

---

## API Documentation

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

## Development Tools

Code formatting

```bash
black .
```

Linting

```bash
ruff check .
```

Type checking

```bash
mypy .
```

Run tests

```bash
pytest
```

---

## Future Improvements

- Refresh token authentication
- Docker support
- CI/CD with GitHub Actions
- Portfolio analytics
- Stock market integration
- Email verification
- Password reset
- Rate limiting
- Pagination and filtering
- API versioning

---

## License

This project is intended for learning and portfolio purposes.