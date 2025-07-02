import sys
import types
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Dummy streamlit module for tests
st_dummy = types.ModuleType('streamlit')
st_dummy.markdown = lambda *a, **k: None
st_dummy.write = lambda *a, **k: None
st_dummy.number_input = lambda *a, **k: 0
st_dummy.button = lambda *a, **k: False
st_dummy.session_state = {}
sys.modules['streamlit'] = st_dummy

from mechanics.inflation_mechanics import InflationMechanics


def test_apply_baseline_weekly_rate():
    im = InflationMechanics()
    im.apply_baseline(days=7)
    assert im.inflation_index == pytest.approx(100 * 1.005, rel=1e-3)


def test_shock_and_reduction():
    im = InflationMechanics()
    im.apply_shock(0.03)
    assert im.inflation_index == pytest.approx(103.0, rel=1e-3)
    im.apply_reduction(0.01)
    assert im.inflation_index == pytest.approx(103.0 * 0.99, rel=1e-3)


def test_recalculate_prices_updates_values():
    im = InflationMechanics()
    im.inflation_index = 110
    items = [{"name": "test", "price": 100, "cost": 50}]
    updated = im.recalculate_prices(items)
    assert updated[0]['price'] == pytest.approx(110)
    assert updated[0]['cost'] == pytest.approx(55)
