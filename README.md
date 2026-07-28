# Finance Portfolio Tracker

A personal finance management system built in Python tracking 
bank accounts, transactions, demat accounts, and investment 
portfolios.

## Tech Stack
Python · PostgreSQL · psycopg2 · SQLAlchemy 2.0 · Alembic · pytest

## Architecture
- **Models** — SQLAlchemy 2.0 ORM with Mapped dataclasses
- **Repositories** — psycopg2 (raw) and SQLAlchemy versions
- **Services** — business logic with custom exception hierarchy
- **Migrations** — Alembic schema versioning

## Database Schema
7 tables: users, bank_accounts, bank_categories, 
bank_transactions, demat_accounts, demat_holdings, 
demat_transactions

## Setup
1. Clone the repo
2. Create virtual environment: python -m venv .venv
3. Install dependencies: pip install -r requirements.txt
4. Copy .env.example to .env and fill in your DB credentials
5. Run migrations: alembic upgrade head
6. Run: python main.py