from dataclasses import dataclass


@dataclass(slots=True)
class CategoryCreate:
    name: str
    description: str


@dataclass(slots=True)
class Category:
    id: int
    name: str
    description: str
