# Investment Portfolio Management System

A Python backend project built using **psycopg2** and **PostgreSQL** to simulate a simple banking and investment portfolio management system.

The primary objective of this project is to practice writing production-style database code without relying on an ORM. The project follows a layered architecture using the Repository Pattern and Service Layer while demonstrating clean code practices, connection pooling, transactions, and business logic.

---

## Features

### User Management

- Create users
- Update user information
- Delete users
- Retrieve users

### Bank Accounts

- Multiple bank accounts per user
- Unique account numbers
- Update account names
- Track balances

### Bank Transactions

- Credit and debit transactions
- Transaction categories
- Balance validation
- Prevent overdrafts

### Demat Accounts

- Multiple brokerage accounts per user
- Unique broker account IDs
- Update account nicknames

### Investment Portfolio

- Holdings for each stock
- Average buy price calculation
- Buy transactions
- Sell transactions
- Prevent selling more shares than owned

---

# Tech Stack

- Python 3.13
- PostgreSQL
- psycopg2
- python-dotenv
- pytest
- Ruff
- Black
- MyPy

---

# Project Structure

```text
project/
│
├── config/
│   └── database_connection.py
│
├── exceptions/
│
├── models/
│
├── repositories/
│
├── services/
│
├── tests/
│
├── requirements.txt
│
└── README.md
```

---

# Architecture

The project follows a layered architecture.

```text
Application
      │
      ▼
Services
      │
      ▼
Repositories
      │
      ▼
PostgreSQL
```

## Repository Layer

Responsible only for database operations.

- CRUD
- SQL queries
- Mapping database rows to models

Repositories contain **no business logic**.

---

## Service Layer

Responsible for business rules.

Examples:

- User validation
- Account existence checks
- Prevent overdrafts
- Prevent selling more shares than owned
- Calculate weighted average buy price
- Coordinate multiple repositories

---

# Database Concepts Demonstrated

- PostgreSQL
- Foreign Keys
- Unique Constraints
- CHECK Constraints
- Transactions
- Connection Pooling
- RealDictCursor
- Context Managers
- Parameterized Queries
- Repository Pattern
- Service Layer
- Custom Exceptions
- Type Hinting

---

# Example Business Logic

## Buying Shares

When additional shares are purchased, the portfolio recalculates the weighted average purchase price.

```
New Average Price =
(
Old Quantity × Old Average Price
+
Purchased Quantity × Purchase Price
)
/
New Quantity
```

---

## Selling Shares

The service validates:

- Portfolio exists
- Enough shares are available

If all shares are sold:

```
Quantity = 0
Average Buy Price = 0
```

---

# Connection Pool

The application uses `psycopg2.pool.SimpleConnectionPool`.

Benefits:

- Reuses database connections
- Improves performance
- Demonstrates production-style connection management

---

# Error Handling

Custom exceptions are used throughout the service layer.

Examples:

- UserNotFoundError
- PortfolioNotFoundError
- InvalidTransactionTypeError
- InsufficientSharesError

---

# Testing

Tests are written using **pytest**.

Run all tests:

```bash
pytest
```

---

# Code Quality

Formatting:

```bash
black .
```

Linting:

```bash
ruff check .
```

Static Type Checking:

```bash
mypy .
```

---

# Installation

Clone the repository.

```bash
git clone https://github.com/yourusername/investment-portfolio-system.git

cd investment-portfolio-system
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it.

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Create a PostgreSQL database.

Copy:

```
.env.example
```

to

```
.env
```

Fill in your database credentials.

Run the project.

---

# Future Improvements

- SQLAlchemy ORM
- Alembic migrations
- FastAPI REST API
- JWT Authentication
- Redis caching
- Docker
- CI/CD
- Async PostgreSQL (asyncpg)

---

# Learning Objectives

This project was built to strengthen understanding of:

- Raw SQL with psycopg2
- PostgreSQL
- Clean Architecture
- Repository Pattern
- Service Layer
- Business Logic
- Connection Pooling
- Database Transactions
- Python Best Practices

---

## License

MIT License