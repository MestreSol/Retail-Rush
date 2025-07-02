import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mechanics.inflation_mechanics import InflationMechanics
from Domain.Entity.Product import Product


def test_basic_inflation_growth():
    im = InflationMechanics(base_weekly_rate=0.007)
    p = Product("1", "Teste", "cat", "sup", 10.0, 20.0, "un")
    for _ in range(7):
        im.apply_inflation([p])
    assert im.current_index > 1.0
    assert p.price > 20.0


def test_shock_increases_rate():
    im = InflationMechanics()
    p = Product("1", "Teste", "cat", "sup", 10.0, 20.0, "un")
    im.apply_inflation([p], shock=True)
    assert im.current_index > 1.03


def test_promotion_reduces_rate():
    im = InflationMechanics()
    p = Product("1", "Teste", "cat", "sup", 10.0, 20.0, "un")
    im.apply_inflation([p], promotion_effect=0.02)
    assert im.current_index < 1.0
