from dataclasses import dataclass

@dataclass
class Currency:
    """Represent a currency with a value relative to a base currency."""

    name: str
    symbol: str
    rate: float = 1.0
