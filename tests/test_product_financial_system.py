import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mechanics.product_financial_system import ProductFinanceSystem
from mechanics.inflation_mechanics import InflationMechanics
from mechanics.currency_mechanics import CurrencyMechanics
from Domain.Entity.Product import Product


def test_integration_price_update_and_conversion():
    p = Product("1", "Teste", "cat", "sup", 10.0, 20.0, "un")
    im = InflationMechanics(base_weekly_rate=0.007)
    cm = CurrencyMechanics()
    cm.add_currency('Dollar', '$', 5.0)
    system = ProductFinanceSystem(im, cm, display_currency='Dollar')

    system.advance_day([p])
    price_in_dollar = system.product_price(p)
    expected = cm.convert(p.price, 'Base', 'Dollar')
    assert price_in_dollar == expected
    assert p.price > 20.0
