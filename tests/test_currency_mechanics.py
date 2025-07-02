import sys
import types
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Minimal dummy for streamlit used in mechanics modules
st_dummy = types.ModuleType('streamlit')
sys.modules['streamlit'] = st_dummy

from mechanics.currency_mechanics import CurrencyMechanics


def test_add_currency():
    cm = CurrencyMechanics()
    cm.add_currency('Dollar', '$', 5.0)
    assert 'Dollar' in cm.currencies
    assert cm.currencies['Dollar'].rate == 5.0


def test_convert_between_currencies():
    cm = CurrencyMechanics()
    cm.add_currency('Dollar', '$', 5.0)
    # 10 Dollars should be 50 in base currency
    assert cm.convert(10, 'Dollar', 'Base') == 50.0
    # 50 base should be 10 Dollars
    assert cm.convert(50, 'Base', 'Dollar') == 10.0
