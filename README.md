# Financial Tracker

A modular backend application for managing personal finances and stock investments, built with **Python**, **PostgreSQL**, and **SQLAlchemy 2.0 ORM**.

The project follows a layered architecture using the **Repository Pattern** and **Service Layer**, providing a clean separation between database access and business logic.

---

## Features

### User Management
- Create, update and delete users
- Retrieve users by ID
- Retrieve all users
- Prevent duplicate email registration

### Bank Accounts
- Create multiple bank accounts per user
- Update account names
- Delete accounts
- View all accounts belonging to a user

### Bank Transactions
- Credit and debit transactions
- Automatic balance updates
- Insufficient balance validation
- Transaction history

### Demat Accounts
- Create and manage brokerage accounts
- Prevent duplicate broker account IDs
- Retrieve accounts by user

### Stock Portfolio
- Buy shares
- Sell shares
- Automatic portfolio quantity updates
- Weighted Average Buy Price calculation
- Prevent selling more shares than owned

---

# Tech Stack

- Python 3.13
- PostgreSQL
- SQLAlchemy 2.0 ORM
- Python Type Hints
- Decimal for financial calculations

---

# Project Structure

```
financial_tracker/
│
├── config/
│   ├── database.py
│   └── settings.py
│
├── models/
│
├── repositories/
│
├── services/
│
├── exceptions/
│
├── schema/
│
└── main.py
```

---

# Architecture

```
                Application
                     │
                     ▼
             Service Layer
      (Business Rules & Validation)
                     │
                     ▼
           Repository Layer
      (Database Access Only)
                     │
                     ▼
           SQLAlchemy 2.0 ORM
                     │
                     ▼
               PostgreSQL
```

---

# Design Principles

- Repository Pattern
- Service Layer Pattern
- Separation of Concerns
- Dependency Injection
- SQLAlchemy Unit of Work
- Transaction Management
- Domain-specific Exceptions

---

# Business Rules

### Users
- Email addresses must be unique.

### Bank Accounts
- User must exist before creating an account.
- Account balance is modified only through transactions.

### Bank Transactions
- Amount must be greater than zero.
- Debit transactions cannot exceed the available balance.
- Credit transactions automatically increase the account balance.

### Demat Accounts
- User must exist before creating a Demat account.
- Broker account IDs must be unique.

### Demat Transactions
- Quantity must be greater than zero.
- Price per share must be greater than zero.
- Sell transactions cannot exceed available holdings.
- Buying shares recalculates the weighted average buy price.
- Selling all shares resets the average buy price to zero.

---

# SQLAlchemy Concepts Practiced

- Declarative Mapping
- SQLAlchemy 2.0 Typed ORM
- Relationships
- Session Management
- Unit of Work Pattern
- CRUD Operations
- Transactions and Rollbacks
- ORM State Tracking
- Repository Pattern
- Service Layer
- Type-safe Models
- Custom Exceptions

---

# Database Relationships

```
User
├── BankAccount
│     └── BankTransaction
│
└── DematAccount
      └── DematHolding
            └── DematTransaction
```

---

# Error Handling

Custom domain exceptions are used throughout the application.

Examples include:

- UserNotFoundError
- DuplicateEmailError
- AccountNotFoundError
- DuplicateAccountNumberError
- CategoryNotFoundError
- InsufficientFundsError
- HoldingNotFoundError
- InsufficientSharesError
- DuplicateBrokerAccountIdError
- InvalidTransactionTypeError

---

# Future Improvements

- Alembic database migrations
- FastAPI REST API
- Redis caching
- JWT Authentication
- Docker support
- Automated testing with Pytest
- CI/CD pipeline
- Portfolio analytics
- Profit/Loss calculations
- Dividend tracking

---

# Learning Outcomes

This project was built to gain practical experience with backend application architecture and SQLAlchemy ORM.

Key topics explored include:

- SQLAlchemy 2.0 ORM
- PostgreSQL integration
- Layered backend architecture
- Repository Pattern
- Service Layer
- Database transactions
- Relationship mapping
- Business logic implementation
- Financial data modeling

---

# Legacy Note

This project originally used **psycopg2** with raw SQL and the Repository Pattern.

It has since been migrated to **SQLAlchemy 2.0 ORM**. Some legacy `psycopg2` modules may still exist in the repository as part of the migration history but are no longer used by the application.