from cattle_lca.database_manager import DataManager
from cattle_lca.models import (
    Animal_Features,
    Grass,
    Concentrate,
    Upstream,
    Emissions_Factors,
)


class Loader:
    def __init__(self, ef_country):
        self.ef_country = ef_country
        self.dataframes = DataManager(ef_country)
        self.grass = self.get_grass()
        self.animal_features = self.get_animal_features()
        self.concentrates = self.get_concentrates()
        self.emissions_factors = self.get_emissions_factors()
        self.upstream = self.get_upstream()

    def get_grass(self):
        return Grass(self.dataframes.grass_data())

    def get_animal_features(self):
        return Animal_Features(self.dataframes.animal_features_data())

    def get_concentrates(self):
        return Concentrate(self.dataframes.concentrate_data())

    def get_emissions_factors(self):
        return Emissions_Factors(self.dataframes.emissions_factor_data())

    def get_upstream(self):
        return Upstream(self.dataframes.upstream_data())
