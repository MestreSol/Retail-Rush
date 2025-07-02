from dataclasses import dataclass, field
from typing import List


@dataclass
class ElectionResult:
    """Election vote percentages for two main candidates."""

    candidate_a: float
    candidate_b: float


@dataclass
class AgeDistribution:
    """Population percentage by age groups."""

    age_0_18: float
    age_19_35: float
    age_36_60: float
    age_60_plus: float


@dataclass
class EthnicityDistribution:
    """Population percentage by ethnicity."""

    white: float
    black: float
    hispanic: float
    asian: float
    other: float


@dataclass
class RegionProfile:
    """Detailed region information used for market simulations."""

    name: str
    currency: str
    sales_tax: float
    population: int
    election: ElectionResult
    age: AgeDistribution
    ethnicity: EthnicityDistribution
    climate: str
    seasons: str
    inflation_base: float
    average_income: float
    preferred_products: List[str] = field(default_factory=list)
