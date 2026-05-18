"""Inventory API — In-memory storage. Contains intentional flaws for experiments."""
from datetime import datetime
from typing import Optional

from .models import Product, ProductStatus, Category, Order, OrderItem


_store = {
    "products": {
        1: Product(1, "Widget A", "SKU-001", 9.99, 100, ProductStatus.ACTIVE, 1),
        2: Product(2, "Gadget B", "SKU-002", 24.99, 50, ProductStatus.ACTIVE, 1),
        3: Product(3, "Doohickey C", "SKU-003", 4.99, 200, ProductStatus.ACTIVE, 2),
    },
    "categories": {
        1: Category(1, "Tools", "Hand tools and equipment"),
        2: Category(2, "Accessories", "Supplementary items"),
    },
    "orders": {},
    "next_id": {"product": 4, "category": 3, "order": 1},
}


def get_product(product_id: int) -> Optional[Product]:
    return _store["products"].get(product_id)


def list_products(category_id: Optional[int] = None,
                  status: Optional[str] = None,
                  min_price: Optional[float] = None,
                  max_price: Optional[float] = None) -> list[Product]:
    results = list(_store["products"].values())
    if category_id:
        results = [p for p in results if p.category_id == category_id]
    if status:
        results = [p for p in results if p.status.value == status]
    if min_price is not None:
        results = [p for p in results if p.price >= min_price]
    if max_price is not None:
        results = [p for p in results if p.price <= max_price]
    return results


def add_product(product: Product) -> Product:
    pid = _store["next_id"]["product"]
    product.id = pid
    product.created_at = datetime.now()
    product.updated_at = datetime.now()
    _store["products"][pid] = product
    _store["next_id"]["product"] = pid + 1
    return product


def update_product(product_id: int, **kwargs) -> Optional[Product]:
    product = get_product(product_id)
    if not product:
        return None
    for key, value in kwargs.items():
        if hasattr(product, key) and value is not None:
            setattr(product, key, value)
    product.updated_at = datetime.now()
    return product


def delete_product(product_id: int) -> bool:
    if product_id in _store["products"]:
        del _store["products"][product_id]
        return True
    return False


# BUG: price validation — allows negative prices
def create_order(items: list[dict]) -> Order:
    order_items = []
    total = 0.0
    for item in items:
        pid = item["product_id"]
        qty = item["quantity"]
        product = get_product(pid)
        if not product:
            raise ValueError(f"Product {pid} not found")
        # BUG: doesn't check stock availability
        unit_price = product.price
        order_items.append(OrderItem(pid, qty, unit_price))
        total += qty * unit_price

    oid = _store["next_id"]["order"]
    order = Order(id=oid, items=order_items, total=round(total, 2))
    _store["orders"][oid] = order
    _store["next_id"]["order"] = oid + 1
    return order


def get_order(order_id: int) -> Optional[Order]:
    return _store["orders"].get(order_id)


def list_categories() -> list[Category]:
    return list(_store["categories"].values())
