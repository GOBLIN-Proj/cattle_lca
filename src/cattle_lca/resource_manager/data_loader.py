"""
Data Loader Module
------------------

This module contains the Loader class, which is responsible for loading and providing access to various data categories required for 
lifecycle assessment (LCA) calculations.
"""

from cattle_lca.resource_manager.database_manager import DataManager
from cattle_lca.resource_manager.models import (
    Animal_Features,
    Grass,
    Concentrate,
    Upstream,
    Emissions_Factors,
)


class Loader:
    """
    The Loader class serves as a data retrieval layer between the data sources and the application logic. 
    It utilizes the DataManager to access different types of environmental and agricultural data based on the specified country's emission factors. 
    This class initializes and provides access to various data categories required for lifecycle assessment (LCA) calculations, 
    such as grass, animal features, concentrates, emissions factors, and upstream data.

    Attributes:
        ef_country (str): A string representing the country for which the emission factors and related data are to be loaded.
        dataframes (DataManager): An instance of DataManager initialized with the country-specific data.
        grass (Grass): An object containing grass-related data.
        animal_features (Animal_Features): An object containing data related to animal features.
        concentrates (Concentrate): An object containing data related to concentrates (animal feed).
        emissions_factors (Emissions_Factors): An object containing various emissions factors data.
        upstream (Upstream): An object containing upstream data related to various inputs and processes.

    Args:
        ef_country (str): The country identifier used to retrieve country-specific data for LCA calculations.

    Methods:
        get_grass(): Initializes and returns an instance of the Grass class containing grass-related data.
        get_animal_features(): Initializes and returns an instance of the Animal_Features class containing data related to animal characteristics.
        get_concentrates(): Initializes and returns an instance of the Concentrate class containing data on animal feed concentrates.
        get_emissions_factors(): Initializes and returns an instance of the Emissions_Factors class containing various emissions factors data.
        get_upstream(): Initializes and returns an instance of the Upstream class containing upstream data related to various inputs and processes.
    """
    def __init__(self, ef_country):
        self.ef_country = ef_country
        self.dataframes = DataManager(ef_country)
        self.grass = self.get_grass()
        self.animal_features = self.get_animal_features()
        self.concentrates = self.get_concentrates()
        self.emissions_factors = self.get_emissions_factors()
        self.upstream = self.get_upstream()


    def get_grass(self):
        """
        Initializes and returns an instance of the Grass class containing grass-related data.

        Returns:
            Grass: An object containing grass-related data.
        """
        return Grass(self.dataframes.grass_data())


    def get_animal_features(self):
        """
        Initializes and returns an instance of the Animal_Features class containing data related to animal characteristics.

        Returns:
            Animal_Features: An object containing data related to animal features.
        """
        return Animal_Features(self.dataframes.animal_features_data())


    def get_concentrates(self):
        """
        Initializes and returns an instance of the Concentrate class containing data on animal feed concentrates.

        Returns:
            Concentrate: An object containing data related to concentrates (animal feed).
        """
        return Concentrate(self.dataframes.concentrate_data())


    def get_emissions_factors(self):
        """
        Initializes and returns an instance of the Emissions_Factors class containing various emissions factors data.

        Returns:
            Emissions_Factors: An object containing various emissions factors data.
        """
        return Emissions_Factors(self.dataframes.emissions_factor_data())


    def get_upstream(self):
        """
        Initializes and returns an instance of the Upstream class containing upstream data related to various inputs and processes.

        Returns:
            Upstream: An object containing upstream data related to various inputs and processes.
        """
        return Upstream(self.dataframes.upstream_data())
