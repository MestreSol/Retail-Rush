import streamlit as st

from Domain.Entity.Currency.currency import Currency


class CurrencyMechanics:
    """Simple currency management and conversion system."""

    def __init__(self):
        # Base currency always has rate 1
        self.currencies: dict[str, Currency] = {
            "Base": Currency(name="Base", symbol="B", rate=1.0)
        }

    def add_currency(self, name: str, symbol: str, rate: float) -> Currency:
        """Add or update a currency."""
        currency = Currency(name=name, symbol=symbol, rate=rate)
        self.currencies[name] = currency
        return currency

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Convert an amount between two currencies."""
        if from_currency not in self.currencies:
            raise ValueError("Unknown currency: " + from_currency)
        if to_currency not in self.currencies:
            raise ValueError("Unknown currency: " + to_currency)

        base_amount = amount * self.currencies[from_currency].rate
        return base_amount / self.currencies[to_currency].rate

    def run(self):
        """Display a simple Streamlit interface for currency management."""
        st.markdown("### 💱 Sistema Monetário")
        st.write("Gerencie moedas e realize conversões.")

        with st.expander("Adicionar Moeda"):
            name = st.text_input("Nome da moeda", key="currency_name")
            symbol = st.text_input("Símbolo", key="currency_symbol")
            rate = st.number_input("Valor em relação à base", value=1.0, key="currency_rate")
            if st.button("Adicionar", key="add_currency_btn") and name:
                self.add_currency(name, symbol, rate)
                st.success(f"Moeda {name} adicionada.")

        st.markdown("### Conversão")
        currencies = list(self.currencies.keys())
        from_curr = st.selectbox("De", currencies, key="from_curr")
        to_curr = st.selectbox("Para", currencies, index=min(1, len(currencies)-1), key="to_curr")
        amount = st.number_input("Quantidade", value=1.0, key="conv_amount")
        if st.button("Converter", key="convert_btn"):
            result = self.convert(amount, from_curr, to_curr)
            st.success(
                f"{amount} {self.currencies[from_curr].symbol} = {result:.2f} {self.currencies[to_curr].symbol}"
            )
