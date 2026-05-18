"""Inventory API — Test suite. Tests that should pass after fixes."""
import pytest
from inventory_api.store import get_product, list_products, add_product, update_product, delete_product, create_order
from inventory_api.models import Product, ProductStatus


class TestProducts:
    def test_get_existing_product(self):
        p = get_product(1)
        assert p is not None
        assert p.name == "Widget A"

    def test_get_nonexistent_product(self):
        assert get_product(999) is None

    def test_list_all(self):
        assert len(list_products()) >= 3

    def test_list_by_category(self):
        results = list_products(category_id=1)
        assert all(p.category_id == 1 for p in results)

    def test_list_by_price_range(self):
        results = list_products(min_price=5.0, max_price=20.0)
        assert all(5.0 <= p.price <= 20.0 for p in results)

    def test_add_product(self):
        p = Product(id=0, name="Test", sku="SKU-TEST", price=1.0,
                    quantity=10, status=ProductStatus.ACTIVE, category_id=1)
        result = add_product(p)
        assert result.id > 0
        assert get_product(result.id) is not None

    def test_update_product(self):
        result = update_product(1, name="Widget A Updated")
        assert result is not None
        assert result.name == "Widget A Updated"
        # Verify persistence
        assert get_product(1).name == "Widget A Updated"
        # Reset
        update_product(1, name="Widget A")

    def test_delete_product(self):
        p = Product(id=0, name="Temp", sku="SKU-TEMP", price=1.0,
                    quantity=1, status=ProductStatus.ACTIVE, category_id=1)
        p = add_product(p)
        assert delete_product(p.id) is True
        assert get_product(p.id) is None

    def test_delete_nonexistent(self):
        assert delete_product(999) is False


class TestOrders:
    def test_create_order(self):
        order = create_order([{"product_id": 1, "quantity": 2}])
        assert order.id >= 1
        assert order.total == 19.98  # 9.99 * 2
        assert len(order.items) == 1

    def test_create_order_multiple_items(self):
        order = create_order([{"product_id": 1, "quantity": 1},
                              {"product_id": 2, "quantity": 3}])
        assert order.total == 9.99 + 24.99 * 3  # = 84.96
        assert len(order.items) == 2

    def test_order_nonexistent_product(self):
        with pytest.raises(ValueError):
            create_order([{"product_id": 999, "quantity": 1}])

    # This test will fail until bug is fixed: no stock check
    def test_order_insufficient_stock(self):
        with pytest.raises(ValueError):
            # Product 1 has quantity=100, ordering 200 should fail
            create_order([{"product_id": 1, "quantity": 200}])
