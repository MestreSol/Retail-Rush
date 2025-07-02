from dataclasses import dataclass
import random
import streamlit as st

@dataclass
class Candidate:
    """Represent a political candidate with economic modifiers."""

    name: str
    tax_modifier: float = 1.0
    regulation_modifier: float = 1.0
    incentive_modifier: float = 1.0


class ElectionMechanics:
    """Simple election system with candidate modifiers."""

    def __init__(self):
        self.candidates = [
            Candidate(
                "Conservador",
                tax_modifier=0.9,
                regulation_modifier=0.8,
                incentive_modifier=0.8,
            ),
            Candidate(
                "Liberal",
                tax_modifier=0.8,
                regulation_modifier=0.6,
                incentive_modifier=1.2,
            ),
            Candidate(
                "Social",
                tax_modifier=1.2,
                regulation_modifier=1.1,
                incentive_modifier=1.0,
            ),
        ]

    def generate_candidate(self, name: str | None = None) -> Candidate:
        """Return a random candidate or one by name."""
        if name:
            for candidate in self.candidates:
                if candidate.name == name:
                    return candidate
        return random.choice(self.candidates)

    def apply_modifiers(self, base_values: dict, candidate: Candidate) -> dict:
        """Apply candidate modifiers to provided values."""
        return {
            "tax": base_values.get("tax", 0) * candidate.tax_modifier,
            "regulation": base_values.get("regulation", 0)
            * candidate.regulation_modifier,
            "incentive": base_values.get("incentive", 0) * candidate.incentive_modifier,
        }

    def run(self):
        """Display interface to generate and apply election modifiers."""
        st.markdown("### 🗳 Eleições")
        st.write("Simule o impacto de diferentes candidatos.")

        if st.button("Sortear Candidato"):
            st.session_state["current_candidate"] = self.generate_candidate()

        candidate = st.session_state.get("current_candidate")
        if candidate:
            st.markdown(f"**Candidato:** {candidate.name}")
            st.markdown(
                f"Modificadores: Tributação x{candidate.tax_modifier}, "
                f"Regulamentação x{candidate.regulation_modifier}, "
                f"Incentivos x{candidate.incentive_modifier}"
            )
            with st.expander("Aplicar em valores de exemplo"):
                tax = st.number_input("Tributação base", value=100.0)
                regulation = st.number_input("Regulamentação base", value=100.0)
                incentive = st.number_input("Incentivos base", value=100.0)
                if st.button("Aplicar Modificadores"):
                    result = self.apply_modifiers(
                        {
                            "tax": tax,
                            "regulation": regulation,
                            "incentive": incentive,
                        },
                        candidate,
                    )
                    st.success(
                        f"Tributação: {result['tax']:.2f} | "
                        f"Regulamentação: {result['regulation']:.2f} | "
                        f"Incentivos: {result['incentive']:.2f}"
                    )
