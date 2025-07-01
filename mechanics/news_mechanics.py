from dataclasses import dataclass
import random
import streamlit as st

@dataclass
class NewsEvent:
    name: str
    price_modifier: float = 1.0
    demand_modifier: float = 1.0
    availability_modifier: float = 1.0
    duration: int = 1


class NewsMechanics:
    """Simple system for random news events affecting market variables."""

    def __init__(self):
        self.events = [
            NewsEvent("Black Friday", price_modifier=0.8, demand_modifier=1.5, availability_modifier=1.2, duration=3),
            NewsEvent("Greve de Transportes", price_modifier=1.1, demand_modifier=0.9, availability_modifier=0.5, duration=5),
            NewsEvent("Lançamento de Produto", price_modifier=1.0, demand_modifier=1.3, availability_modifier=1.0, duration=2),
        ]

    def generate_event(self, name: str | None = None) -> NewsEvent:
        """Return a random event or one by name."""
        if name:
            for event in self.events:
                if event.name == name:
                    return event
        return random.choice(self.events)

    def apply_modifiers(self, base_values: dict, event: NewsEvent) -> dict:
        """Apply event modifiers to a dict with price, demand and availability."""
        return {
            "price": base_values.get("price", 0) * event.price_modifier,
            "demand": base_values.get("demand", 0) * event.demand_modifier,
            "availability": base_values.get("availability", 0) * event.availability_modifier,
        }

    def run(self):
        """Display interface to generate and apply news events."""
        st.markdown("### 📰 Notícias e Eventos")
        st.write("Gere eventos aleatórios que afetam o mercado.")

        if st.button("Gerar Evento"):
            st.session_state["current_event"] = self.generate_event()

        event = st.session_state.get("current_event")
        if event:
            st.markdown(f"**Evento:** {event.name}")
            st.markdown(
                f"Modificadores: Preço x{event.price_modifier}, "
                f"Demanda x{event.demand_modifier}, "
                f"Disponibilidade x{event.availability_modifier}"
            )
            st.markdown(f"Duração: {event.duration} dias")

            with st.expander("Aplicar em valores de exemplo"):
                price = st.number_input("Preço base", value=100.0)
                demand = st.number_input("Demanda base", value=100.0)
                availability = st.number_input("Disponibilidade base", value=100.0)
                if st.button("Aplicar Modificadores"):
                    result = self.apply_modifiers({
                        "price": price,
                        "demand": demand,
                        "availability": availability,
                    }, event)
                    st.success(
                        f"Preço: {result['price']:.2f} | "
                        f"Demanda: {result['demand']:.2f} | "
                        f"Disponibilidade: {result['availability']:.2f}"
                    )
