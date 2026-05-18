"""Inventory API — Data models. Seed version with known bugs for experiments."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class ProductStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"


@dataclass
class Product:
    id: int
    name: str
    sku: str
    price: float
    quantity: int
    status: ProductStatus
    category_id: int
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class Category:
    id: int
    name: str
    description: str = ""


@dataclass
class Order:
    id: int
    items: list["OrderItem"] = field(default_factory=list)
    total: float = 0.0
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class OrderItem:
    product_id: int
    quantity: int
    unit_price: float

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price
