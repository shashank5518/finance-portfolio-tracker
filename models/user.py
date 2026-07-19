from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class UserCreate:
    name: str
    email: str
    password_hash: str


@dataclass(slots=True)
class User:
    id: int
    name: str
    email: str
    password_hash: str
    created_at: datetime
