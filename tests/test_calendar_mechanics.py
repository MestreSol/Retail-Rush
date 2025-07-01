import sys
import types
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st_dummy = types.ModuleType('streamlit')
sys.modules['streamlit'] = st_dummy

plotly_dummy = types.ModuleType('plotly')
graph_objects_dummy = types.ModuleType("plotly.graph_objects")
subplots_dummy = types.ModuleType("plotly.subplots")
plotly_dummy.graph_objects = graph_objects_dummy
plotly_dummy.subplots = subplots_dummy
sys.modules["plotly"] = plotly_dummy
sys.modules["plotly.graph_objects"] = graph_objects_dummy
sys.modules["plotly.subplots"] = subplots_dummy
subplots_dummy.make_subplots = lambda *a, **k: None

class DummyDataFrame(list):
    def __init__(self, data):
        super().__init__(data)
        self.columns = []

    @property
    def empty(self):
        return len(self) == 0

pd_dummy = types.ModuleType("pandas")
pd_dummy.DataFrame = DummyDataFrame
sys.modules["pandas"] = pd_dummy

from mechanics.calendar_mechanics import CalendarMechanics


def test_generate_calendar_data_with_tuple_config():
    cm = CalendarMechanics()
    # Should not raise an exception
    data = cm.generate_calendar_data(season_config=[("Spring", 90, "\U0001F331")])
    assert len(data) > 0