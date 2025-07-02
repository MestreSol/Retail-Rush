import math
import streamlit as st


class InflationMechanics:
    """Handle inflation index and price adjustments."""

    def __init__(self, baseline_weekly_rate: float = 0.005):
        # convert weekly rate to daily compound rate
        self.baseline_daily_rate = (1 + baseline_weekly_rate) ** (1 / 7) - 1
        self.base_index = 100.0
        self.inflation_index = 100.0

    def apply_baseline(self, days: int = 1) -> None:
        """Apply baseline inflation for the given number of days."""
        self.inflation_index *= (1 + self.baseline_daily_rate) ** days

    def apply_shock(self, percent: float = 0.03) -> None:
        """Apply an inflation shock (positive percentage)."""
        self.inflation_index *= 1 + percent

    def apply_reduction(self, percent: float = 0.01) -> None:
        """Apply a temporary reduction to the inflation index."""
        self.inflation_index *= max(0.0, 1 - percent)

    def recalculate_prices(self, items: list[dict]) -> list[dict]:
        """Return new prices and costs adjusted by the inflation index."""
        multiplier = self.inflation_index / self.base_index
        updated = []
        for item in items:
            new_item = item.copy()
            if 'price' in item:
                new_item['price'] = item['price'] * multiplier
            if 'cost' in item:
                new_item['cost'] = item['cost'] * multiplier
            updated.append(new_item)
        return updated

    def run(self) -> None:
        """Simple Streamlit interface for adjusting inflation."""
        st.markdown("### Sistema de Inflação")
        st.write(f"Índice atual: {self.inflation_index:.2f}")

        days = st.number_input("Dias para aplicar inflação básica", value=1, min_value=1)
        if st.button("Aplicar inflação semanal"):
            self.apply_baseline(int(days))

        shock = st.number_input("Choque de inflação (%)", value=3.0)
        if st.button("Aplicar choque"):
            self.apply_shock(shock / 100)

        reduction = st.number_input("Redução temporária (%)", value=1.0)
        if st.button("Aplicar redução"):
            self.apply_reduction(reduction / 100)

        st.write(f"Índice atualizado: {self.inflation_index:.2f}")
