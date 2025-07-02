from __future__ import annotations

from dataclasses import asdict
import pandas as pd
import streamlit as st

from Domain.Entity.Map.region_profile import (
    RegionProfile,
    ElectionResult,
    AgeDistribution,
    EthnicityDistribution,
)


class RegionMechanics:
    """Handle predefined region profiles for tabletop tests."""

    def __init__(self):
        self.regions = self._create_regions()

    def _create_regions(self) -> dict[str, RegionProfile]:
        """Return example region profiles for U.S. cities."""
        return {
            "NYC": RegionProfile(
                name="New York City",
                currency="USD",
                sales_tax=0.08875,
                population=8000000,
                election=ElectionResult(candidate_a=60.0, candidate_b=40.0),
                age=AgeDistribution(20.0, 30.0, 35.0, 15.0),
                ethnicity=EthnicityDistribution(42.0, 24.0, 29.0, 14.0, 5.0),
                climate="nublado",
                seasons="invernos frios, verões quentes",
                inflation_base=1.1,
                average_income=65000,
                preferred_products=["café quente", "guarda-chuva"],
            ),
            "LA": RegionProfile(
                name="Los Angeles",
                currency="USD",
                sales_tax=0.095,
                population=3900000,
                election=ElectionResult(candidate_a=55.0, candidate_b=45.0),
                age=AgeDistribution(23.0, 31.0, 33.0, 13.0),
                ethnicity=EthnicityDistribution(29.0, 8.0, 49.0, 11.0, 3.0),
                climate="ensolarado",
                seasons="verões longos e secos",
                inflation_base=1.0,
                average_income=62000,
                preferred_products=["sorvete", "óculos de sol"],
            ),
            "CHI": RegionProfile(
                name="Chicago",
                currency="USD",
                sales_tax=0.1025,
                population=2700000,
                election=ElectionResult(candidate_a=58.0, candidate_b=42.0),
                age=AgeDistribution(22.0, 29.0, 34.0, 15.0),
                ethnicity=EthnicityDistribution(33.0, 29.0, 29.0, 7.0, 2.0),
                climate="nevado",
                seasons="invernos rigorosos, verões amenos",
                inflation_base=1.2,
                average_income=55000,
                preferred_products=["chocolate quente", "agasalhos"],
            ),
        }

    def run(self):
        """Render a simple Streamlit UI to inspect regions."""
        st.markdown("### 🌐 Sistema de Regiões")
        st.write(
            "Perfis geográficos que impactam demanda, preço e logística."
        )
        region_keys = list(self.regions.keys())
        selection = st.selectbox(
            "Escolha a região", [self.regions[k].name for k in region_keys]
        )
        region = next(r for r in self.regions.values() if r.name == selection)

        with st.expander("Detalhes", expanded=True):
            data = asdict(region)
            df = (
                pd.DataFrame(list(data.items()), columns=["Propriedade", "Valor"])
                .astype(str)
            )
            st.dataframe(df, use_container_width=True)


