import random
from Domain.Entity.Map.region_type import region_type


class Region:
    def __init__(self, code, name, majority, population, currency):
        self.code = code
        self.name = name
        self.majority = majority
        self.population = population
        self.currency = currency
        self.currency_value = 1.0
        self.temperature = random.randint(-5, 35)
        # os grupos estão dentro do total da população, esse valor n pode superar
        self.groups = {
            "Children": 0.2 * population,
            "Adults": 0.5 * population,
            "Seniors": 0.3 * population
        }


    @property
    def region_type(self):
        mapping = {
            "Rural": region_type.Rural,
            "Urban": region_type.Urban,
            "Suburban": region_type.Suburban,
            "Coastal": region_type.Coastal,
            "Mountainous": region_type.Mountainous,
            "Desert": region_type.Desert,
            "Forested": region_type.Forested,
            "Industrial": region_type.Industrial,
            "Agricultural": region_type.Agricultural,
            "Arctic": region_type.Arctic,
            "Tropical": region_type.Tropical,
            "Wetland": region_type.Wetland,
            "Highland": region_type.Highland,
            "Metropolitan": region_type.Metropolitan,
            "University": region_type.University,
            "Commercial": region_type.Commercial,
            "Residential": region_type.Residential
        }
        return mapping.get(self.code, None)

