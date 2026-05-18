"""Inventory API — Experiment tasks definition."""
import json

TASKS = [
    # ── Simple tasks (≥ 80% Fast Path expected) ──
    {
        "id": "S1",
        "difficulty": "simple",
        "description": "Add a 'description' field (str, optional) to the Product dataclass and ensure it is preserved through all CRUD operations.",
        "files": ["models.py", "store.py"],
        "expected_fast": True,
    },
    {
        "id": "S2",
        "difficulty": "simple",
        "description": "Fix the bug in store.py where negative prices are allowed. Add validation in add_product() and update_product() to reject prices < 0 with a ValueError.",
        "files": ["store.py"],
        "expected_fast": True,
    },
    {
        "id": "S3",
        "difficulty": "simple",
        "description": "Add a 'tags' field (list[str]) to the Product model. Update the add_product and update_product functions to handle tags. Update list_products to accept an optional 'tag' filter parameter.",
        "files": ["models.py", "store.py"],
        "expected_fast": True,
    },
    {
        "id": "S4",
        "difficulty": "simple",
        "description": "Rename the 'sku' field to 'product_code' on the Product model. Update all references in store.py and tests.",
        "files": ["models.py", "store.py", "test_api.py"],
        "expected_fast": True,
    },
    # ── Complex tasks (should trigger Slow Path upgrade) ──
    {
        "id": "C1",
        "difficulty": "complex",
        "description": "Fix the stock-check bug: before creating an order, verify each product has sufficient quantity. Deduct the ordered quantity from stock after successful order creation. Add a test that verifies insufficient stock raises ValueError and that stock is correctly deducted.",
        "files": ["store.py", "test_api.py"],
        "expected_fast": False,
    },
    {
        "id": "C2",
        "difficulty": "complex",
        "description": "Implement a discount system: add a 'Discount' dataclass (id, name, type='percentage'|'fixed', value, min_order_amount). Add a function apply_discount(order, discount_code) that calculates the discounted total. Discounts cannot stack. Add tests.",
        "files": ["models.py", "store.py", "test_api.py"],
        "expected_fast": False,
    },
    {
        "id": "C3",
        "difficulty": "complex",
        "description": "Add pagination support to list_products(). Accept 'page' (int, default 1) and 'page_size' (int, default 20) parameters. Return a dict with 'items', 'total', 'page', 'page_size', 'total_pages'. Update tests.",
        "files": ["store.py", "test_api.py"],
        "expected_fast": False,
    },
    {
        "id": "C4",
        "difficulty": "complex",
        "description": "Implement an audit log system: whenever a product is added/updated/deleted or an order is created, record the action in an in-memory audit log with timestamp, action_type, entity_type, entity_id, and details (dict). Add a function get_audit_log(entity_type=None, entity_id=None) for filtering. Add tests.",
        "files": ["store.py", "test_api.py"],
        "expected_fast": False,
    },
]

if __name__ == "__main__":
    print(json.dumps(TASKS, indent=2, ensure_ascii=False))
