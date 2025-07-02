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

from mechanics.election_mechanics import ElectionMechanics, Candidate


def test_generate_candidate_returns_known_candidate():
    em = ElectionMechanics()
    candidate = em.generate_candidate()
    assert isinstance(candidate, Candidate)
    assert candidate in em.candidates


def test_apply_modifiers_calculates_values():
    em = ElectionMechanics()
    candidate = Candidate('Teste', 2.0, 0.5, 1.5)
    result = em.apply_modifiers({'tax': 10, 'regulation': 20, 'incentive': 30}, candidate)
    assert result['tax'] == 20
    assert result['regulation'] == 10
    assert result['incentive'] == 45
