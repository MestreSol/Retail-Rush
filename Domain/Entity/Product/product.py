from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Product:
    """Basic representation of a product sold in the supermarket."""

    sku: str
    name: str
    category: str
    supplier: str
    cost: float
    price: float
    unit: str
    storage: Optional[str] = None
    seasonal_months: List[int] = field(default_factory=list)
    shelf_life: Optional[int] = None  # days until expiration
