import sys
import types
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st_dummy = types.ModuleType('streamlit')
st_dummy.markdown = lambda *a, **k: None
st_dummy.write = lambda *a, **k: None
st_dummy.button = lambda *a, **k: False
st_dummy.expander = lambda *a, **k: types.SimpleNamespace(__enter__=lambda self: None, __exit__=lambda self, exc_type, exc, tb: None)
st_dummy.number_input = lambda *a, **k: 0
st_dummy.success = lambda *a, **k: None
st_dummy.session_state = {}
sys.modules['streamlit'] = st_dummy

from mechanics.news_mechanics import NewsMechanics, NewsEvent


def test_generate_event_returns_known_event():
    nm = NewsMechanics()
    event = nm.generate_event()
    assert isinstance(event, NewsEvent)
    assert event in nm.events


def test_apply_modifiers_calculates_values():
    nm = NewsMechanics()
    event = NewsEvent('Teste', 2.0, 0.5, 1.5, 1)
    result = nm.apply_modifiers({'price': 10, 'demand': 20, 'availability': 30}, event)
    assert result['price'] == 20
    assert result['demand'] == 10
    assert result['availability'] == 45
