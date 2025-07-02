# Simple inflation system for Retail Rush
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from Domain.Entity.Product import Product


@dataclass
class DailyRecord:
    """Store daily inflation index history."""

    day: int
    index: float


class InflationMechanics:
    """Simulate continuous price variation over time."""

    def __init__(self, base_weekly_rate: float = 0.005):
        # Base weekly inflation rate (e.g. 0.5% -> 0.005)
        self.base_weekly_rate = base_weekly_rate
        self.current_index = 1.0
        self.day_count = 0
        self.history: List[DailyRecord] = []

    def advance_day(self, shock: bool = False, promotion_effect: float = 0.0) -> float:
        """Advance one day applying inflation, shocks and promotions."""
        daily_rate = self.base_weekly_rate / 7
        if shock:
            daily_rate += 0.03  # abrupt 3% increase
        daily_rate -= promotion_effect

        self.current_index *= 1 + daily_rate
        self.day_count += 1
        self.history.append(DailyRecord(self.day_count, self.current_index))
        return daily_rate

    def apply_inflation(self, products: List[Product], shock: bool = False, promotion_effect: float = 0.0) -> None:
        """Update product prices and costs based on today's inflation."""
        daily_rate = self.advance_day(shock=shock, promotion_effect=promotion_effect)
        for prod in products:
            prod.cost *= 1 + daily_rate
            prod.price *= 1 + daily_rate

    def adjust_purchasing_power(self, income: float) -> float:
        """Return income adjusted by accumulated inflation."""
        return income / self.current_index
