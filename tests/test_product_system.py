import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Domain.Entity.Product import Product, Inventory
from datetime import date, timedelta


def test_product_creation():
    p = Product(
        sku="001",
        name="Maça",
        category="hortifruti",
        supplier="Fornecedor X",
        cost=1.0,
        price=2.0,
        unit="kg",
        seasonal_months=[11, 0, 1],
        shelf_life=10,
    )
    assert p.sku == "001"
    assert p.seasonal_months == [11, 0, 1]


def test_inventory_basic_flow():
    p = Product(
        sku="001",
        name="Maça",
        category="hortifruti",
        supplier="Fornecedor X",
        cost=1.0,
        price=2.0,
        unit="kg",
    )
    inv = Inventory()
    today = date.today()
    inv.add_stock(p, 5, expiration=today + timedelta(days=5))
    assert inv.get_quantity("001") == 5
    removed = inv.remove_stock("001", 2)
    assert removed == 2
    assert inv.get_quantity("001") == 3
    inv.discard_expired(today + timedelta(days=6))
    assert inv.get_quantity("001") == 0
