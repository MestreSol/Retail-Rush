import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Minimal streamlit stub
import types
st_dummy = types.ModuleType('streamlit')
st_dummy.markdown = lambda *a, **k: None
st_dummy.write = lambda *a, **k: None
st_dummy.selectbox = lambda label, options: options[0]
st_dummy.expander = lambda *a, **k: types.SimpleNamespace(__enter__=lambda self: None, __exit__=lambda self, exc_type, exc, tb: None)
st_dummy.dataframe = lambda *a, **k: None
sys.modules['streamlit'] = st_dummy

import pandas as pd
sys.modules['pandas'] = pd

from mechanics.region_mechanics import RegionMechanics


def test_regions_created():
    rm = RegionMechanics()
    assert set(rm.regions.keys()) == {"NYC", "LA", "CHI"}


def test_election_sum_to_100():
    rm = RegionMechanics()
    for region in rm.regions.values():
        total = region.election.candidate_a + region.election.candidate_b
        assert abs(total - 100.0) < 0.001


def test_climate_field():
    rm = RegionMechanics()
    allowed = {"ensolarado", "nublado", "nevado"}
    for region in rm.regions.values():
        assert region.climate in allowed

