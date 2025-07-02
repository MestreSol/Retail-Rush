from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Dict, List, Optional

from .product import Product


@dataclass
class StockEntry:
    product: Product
    quantity: int
    expiration: Optional[date] = None


class Inventory:
    """Manage product stock and basic replenishment logic."""

    def __init__(self) -> None:
        self._stock: Dict[str, List[StockEntry]] = {}

    def add_stock(self, product: Product, quantity: int, expiration: Optional[date] = None) -> None:
        entries = self._stock.setdefault(product.sku, [])
        entries.append(StockEntry(product, quantity, expiration))

    def remove_stock(self, sku: str, quantity: int) -> int:
        """Remove quantity from available stock. Returns actually removed quantity."""
        removed = 0
        if sku not in self._stock:
            return removed
        entries = self._stock[sku]
        while entries and removed < quantity:
            entry = entries[0]
            take = min(entry.quantity, quantity - removed)
            entry.quantity -= take
            removed += take
            if entry.quantity == 0:
                entries.pop(0)
        if not entries:
            self._stock.pop(sku, None)
        return removed

    def get_quantity(self, sku: str) -> int:
        return sum(entry.quantity for entry in self._stock.get(sku, []))

    def discard_expired(self, today: date) -> None:
        for sku, entries in list(self._stock.items()):
            new_entries = [e for e in entries if not e.expiration or e.expiration >= today]
            if new_entries:
                self._stock[sku] = new_entries
            else:
                self._stock.pop(sku)

    def needs_restock(self, sku: str, min_level: int) -> bool:
        return self.get_quantity(sku) < min_level
