"""
Models Module
-------------

This module contains classes for representing and manipulating dynamic data structures used in livestock data management, specifically for lifecycle assessment in cattle farming. It includes classes for handling animal data, emissions factors, grass data, concentrate data, and upstream data.

Classes:
    DynamicData: A base class for creating objects that hold dynamic data.
    AnimalCategory: Represents different categories of animals on a farm, inheriting from DynamicData.
    AnimalCollection: Represents a collection of animal categories, inheriting from DynamicData.
    Farm: Represents a farm entity, inheriting from DynamicData.
    Animal_Features: Contains all features related to animals used in lifecycle assessment.
    Emissions_Factors: Holds emissions factors data relevant to lifecycle assessment.
    Grass: Contains data about different types of grasses.
    Concentrate: Contains data about different types of animal feed concentrates.
    Upstream: Contains upstream data such as resources used and emissions released before reaching the farm.

Functions:
    load_grass_data(): Loads and returns grass data.
    load_concentrate_data(): Loads and returns concentrate data.
    load_upstream_data(): Loads and returns upstream data.
    load_emissions_factors_data(): Loads and returns emissions factors data.
    load_animal_features_data(): Loads and returns animal features data.
    load_farm_data(farm_data_frame): Takes a DataFrame and returns a dictionary of Farm objects.
    load_livestock_data(animal_data_frame): Takes a DataFrame and returns a dictionary of AnimalCollection objects mapped by farm ID.
    print_livestock_data(data): Utility function to print livestock data for debugging or logging.

The classes mainly serve as containers for the data loaded from external sources like databases or CSV files, enabling structured access and manipulation of this data within the lifecycle assessment processes.
"""
import pandas
import copy


class DynamicData(object):
    """
    A base class for creating dynamic data objects. This class is designed to create instances with attributes
    that are dynamically assigned based on input data. It allows for the easy creation and manipulation of
    data objects without needing a predefined class structure.

    Attributes are set based on two inputs: a defaults dictionary and a data dictionary. The defaults dictionary
    provides initial values for attributes, ensuring that the object has all necessary attributes with default values.
    The data dictionary contains actual values meant to override these defaults where applicable.

    Parameters:
        data (dict): A dictionary containing actual values for attributes of the instance. Keys correspond to attribute
                     names, and values correspond to the values those attributes should take.
        defaults (dict, optional): A dictionary containing default values for attributes of the instance. Keys
                                   correspond to attribute names, and values are the default values those attributes
                                   should take. Defaults to an empty dictionary if not provided.

    """
    def __init__(self, data, defaults={}):
        # Set the defaults first
        for variable, value in defaults.items():
            setattr(self, variable, value)

        # Overwrite the defaults with the real values
        for variable, value in data.items():
            setattr(self, variable, value)


class AnimalCategory(DynamicData):
    """
    A specialized data container class for animal categories, extending DynamicData. This class is designed
    to store and manage information specific to different types of animals.
    It predefines a set of attributes with default values relevant to animal data management.

    Inherits from:
        DynamicData: Inherits the capability to dynamically set attributes based on input data.

    Default Attributes (and their default values):
        pop (int): Population count of the animals in this category (default: 0).
        daily_milk (float): Average daily milk production per animal, in litres (default: 0.0).
        weight (float): Average weight per animal, in kilograms (default: 0.0).
        forage (str): Type of forage consumed by the animals (default: 'average').
        grazing (str): Type of grazing condition (default: 'pasture').
        con_type (str): Type of concentrate feed provided (default: 'concentrate').
        con_amount (float): Amount of concentrate feed provided per day, in kilograms (default: 0.0).
        t_outdoors (int): Average time spent outdoors per day, in hours (default: 24).
        t_indoors (int): Average time spent indoors per day, in hours (default: 0).
        t_stabled (int): Average time spent in stable conditions per day, in hours (default: 0).
        mm_storage (str): Type of manure management storage system (default: 'solid').
        daily_spreading (str): Type of manure spreading technique used daily (default: 'none').
        n_sold (int): Number of animals sold from this category (default: 0).
        n_bought (int): Number of animals bought into this category (default: 0).

    Parameters:
        data (dict): A dictionary containing actual values for attributes of the animal category. Keys correspond
                     to attribute names, and values correspond to the values those attributes should take.

    """
    def __init__(self, data):
        defaults = {
            "pop": 0,
            "daily_milk": 0,
            "weight": 0,
            "forage": "average",
            "grazing": "pasture",
            "con_type": "concentrate",
            "con_amount": 0,
            "t_outdoors": 24,
            "t_indoors": 0,
            "t_stabled": 0,
            "mm_storage": "solid",
            "daily_spreading": "none",
            "n_sold": 0,
            "n_bought": 0,
        }

        super(AnimalCategory, self).__init__(data, defaults)


class AnimalCollection(DynamicData):#
    """
    A data container class for a collection of animal categories. It extends the
    DynamicData class to enable dynamic attribute assignment based on input data, typically used to represent a group
    of animals categorized by species, age, or other criteria.

    Inherits from:
        DynamicData: Inherits the capability to dynamically set attributes based on input data.

    Parameters:
        data (dict): A dictionary where keys represent category names or identifiers, and values are instances of
                     AnimalCategory or similar data structures that hold information specific to each animal group.

    """
    def __init__(self, data):
        super(AnimalCollection, self).__init__(data)


class Farm(DynamicData):
    """
    A data container class representing a "farm", or similar unit, extending the DynamicData class to enable dynamic attribute assignment
    based on input data. This class is typically used to encapsulate all relevant information about a "farm", including
    details about various animal collections, resources, and management practices.

    Inherits from:
        DynamicData: Inherits the capability to dynamically set attributes based on input data.

    Parameters:
        data (dict): A dictionary containing attributes and values that represent various aspects of the farm. This
                     can include information such as the farm's ID, location, size, and any specific animal collections
                     associated with the farm.
    """
    def __init__(self, data):  # , animal_collections):
        # self.animals = animal_collections.get(data.get("farm_id"))

        super(Farm, self).__init__(data)


######################################################################################
# Animal Features Data
######################################################################################
class Animal_Features(object):
    """
    A class that encapsulates various features and statistical data related to different categories of farm animals.
    This class is designed to store and provide access to a wide array of information concerning animal characteristics,
    such as weight gain, nitrogen retention, and mature weight for different animal categories like dairy cows,
    suckler cows, bulls, and various calf types.

    Attributes:
        data_frame (pandas.DataFrame): A DataFrame containing animal features data.
        animal_features (dict): A dictionary storing all the animal features with keys representing the feature names
                                and values representing the corresponding data extracted from the DataFrame.

    Parameters:
        data (pandas.DataFrame): The DataFrame containing the animal features data. Expected to contain columns such as
                                 'birth_weight', 'mature_weight_bulls', 'dairy_cows_weight_gain', etc., with each row
                                 representing a different set of animal feature values.

    Methods:
        Various getter methods for each animal feature, such as get_birth_weight(), get_mature_weight_bulls(), etc.,
        which return the respective values from the animal_features dictionary.

    Usage:
        # Assuming animal_features_df is a pandas DataFrame containing the relevant animal features data
        animal_features = Animal_Features(animal_features_df)
        mature_weight = animal_features.get_mature_weight_dairy_cows()
    """
    def __init__(self, data):
        self.data_frame = data

        self.animal_features = {}

        for _, row in self.data_frame.iterrows():
            birth_weight = row.get("birth_weight")
            mature_weight_bulls = row.get("mature_weight_bulls")
            mature_weight_dairy_cows = row.get("mature_weight_dairy_cows")
            mature_weight_suckler_cows = row.get("mature_weight_suckler_cows")
            dairy_cows_weight_gain = row.get("dairy_cows_weight_gain")
            suckler_cows_weight_gain = row.get("suckler_cows_weight_gain")
            DxD_calves_f_weight_gain = row.get("DxD_calves_f_weight_gain")
            DxD_calves_m_weight_gain = row.get("DxD_calves_m_weight_gain")
            DxB_calves_f_weight_gain = row.get("DxB_calves_f_weight_gain")
            DxB_calves_m_weight_gain = row.get("DxB_calves_f_weight_gain")
            BxB_calves_m_weight_gain = row.get("BxB_calves_m_weight_gain")
            BxB_calves_f_weight_gain = row.get("BxB_calves_f_weight_gain")
            DxD_heifers_less_2_yr_weight_gain = row.get(
                "DxD_heifers_less_2_yr_weight_gain"
            )
            DxD_steers_less_2_yr_weight_gain = row.get(
                "DxD_steers_less_2_yr_weight_gain"
            )
            DxB_heifers_less_2_yr_weight_gain = row.get(
                "DxB_heifers_less_2_yr_weight_gain"
            )
            DxB_steers_less_2_yr_weight_gain = row.get(
                "DxB_steers_less_2_yr_weight_gain"
            )
            BxB_heifers_less_2_yr_weight_gain = row.get(
                "BxB_heifers_less_2_yr_weight_gain"
            )
            BxB_steers_less_2_yr_weight_gain = row.get(
                "BxB_steers_less_2_yr_weight_gain"
            )
            DxD_heifers_more_2_yr_weight_gain = row.get(
                "DxD_heifers_more_2_yr_weight_gain"
            )
            DxD_steers_more_2_yr_weight_gain = row.get(
                "DxD_steers_more_2_yr_weight_gain"
            )
            DxB_heifers_more_2_yr_weight_gain = row.get(
                "DxB_heifers_more_2_yr_weight_gain"
            )
            DxB_steers_more_2_yr_weight_gain = row.get(
                "DxB_steers_more_2_yr_weight_gain"
            )
            BxB_heifers_more_2_yr_weight_gain = row.get(
                "BxB_heifers_more_2_yr_weight_gain"
            )
            BxB_steers_more_2_yr_weight_gain = row.get(
                "BxB_steers_more_2_yr_weight_gain"
            )
            bulls_weight_gain = row.get("bulls_weight_gain")
            dairy_cows_n_retention = row.get("dairy_cows_n_retention")
            suckler_cows_n_retention = row.get("suckler_cows_n_retention")
            DxD_calves_f_n_retention = row.get("DxD_calves_f_n_retention")
            DxD_calves_m_n_retention = row.get("DxD_calves_m_n_retention")
            DxB_calves_f_n_retention = row.get("DxB_calves_f_n_retention")
            DxB_calves_m_n_retention = row.get("DxB_calves_f_n_retention")
            BxB_calves_m_n_retention = row.get("BxB_calves_m_n_retention")
            BxB_calves_f_n_retention = row.get("BxB_calves_f_n_retention")
            DxD_heifers_less_2_yr_n_retention = row.get(
                "DxD_heifers_less_2_yr_n_retention"
            )
            DxD_steers_less_2_yr_n_retention = row.get(
                "DxD_steers_less_2_yr_n_retention"
            )
            DxB_heifers_less_2_yr_n_retention = row.get(
                "DxB_heifers_less_2_yr_n_retention"
            )
            DxB_steers_less_2_yr_n_retention = row.get(
                "DxB_steers_less_2_yr_n_retention"
            )
            BxB_heifers_less_2_yr_n_retention = row.get(
                "BxB_heifers_less_2_yr_n_retention"
            )
            BxB_steers_less_2_yr_n_retention = row.get(
                "BxB_steers_less_2_yr_n_retention"
            )
            DxD_heifers_more_2_yr_n_retention = row.get(
                "DxD_heifers_more_2_yr_n_retention"
            )
            DxD_steers_more_2_yr_n_retention = row.get(
                "DxD_steers_more_2_yr_n_retention"
            )
            DxB_heifers_more_2_yr_n_retention = row.get(
                "DxB_heifers_more_2_yr_n_retention"
            )
            DxB_steers_more_2_yr_n_retention = row.get(
                "DxB_steers_more_2_yr_n_retention"
            )
            BxB_heifers_more_2_yr_n_retention = row.get(
                "BxB_heifers_more_2_yr_n_retention"
            )
            BxB_steers_more_2_yr_n_retention = row.get(
                "BxB_steers_more_2_yr_n_retention"
            )
            bulls_n_retention = row.get("bulls_n_retention")

            self.animal_features = {
                "birth_weight": birth_weight,
                "mature_weight_bulls": mature_weight_bulls,
                "mature_weight_dairy_cows": mature_weight_dairy_cows,
                "mature_weight_suckler_cows": mature_weight_suckler_cows,
                "dairy_cows_weight_gain": dairy_cows_weight_gain,
                "suckler_cows_weight_gain": suckler_cows_weight_gain,
                "DxD_calves_f_weight_gain": DxD_calves_f_weight_gain,
                "DxD_calves_m_weight_gain": DxD_calves_m_weight_gain,
                "DxB_calves_f_weight_gain": DxB_calves_f_weight_gain,
                "DxB_calves_m_weight_gain": DxB_calves_m_weight_gain,
                "BxB_calves_m_weight_gain": BxB_calves_m_weight_gain,
                "BxB_calves_f_weight_gain": BxB_calves_f_weight_gain,
                "DxD_heifers_less_2_yr_weight_gain": DxD_heifers_less_2_yr_weight_gain,
                "DxD_steers_less_2_yr_weight_gain": DxD_steers_less_2_yr_weight_gain,
                "DxB_heifers_less_2_yr_weight_gain": DxB_heifers_less_2_yr_weight_gain,
                "DxB_steers_less_2_yr_weight_gain": DxB_steers_less_2_yr_weight_gain,
                "BxB_heifers_less_2_yr_weight_gain": BxB_heifers_less_2_yr_weight_gain,
                "BxB_steers_less_2_yr_weight_gain": BxB_steers_less_2_yr_weight_gain,
                "DxD_heifers_more_2_yr_weight_gain": DxD_heifers_more_2_yr_weight_gain,
                "DxD_steers_more_2_yr_weight_gain": DxD_steers_more_2_yr_weight_gain,
                "DxB_heifers_more_2_yr_weight_gain": DxB_heifers_more_2_yr_weight_gain,
                "DxB_steers_more_2_yr_weight_gain": DxB_steers_more_2_yr_weight_gain,
                "BxB_heifers_more_2_yr_weight_gain": BxB_heifers_more_2_yr_weight_gain,
                "BxB_steers_more_2_yr_weight_gain": BxB_steers_more_2_yr_weight_gain,
                "bulls_weight_gain": bulls_weight_gain,
                "dairy_cows_n_retention": dairy_cows_n_retention,
                "suckler_cows_n_retention": suckler_cows_n_retention,
                "DxD_calves_f_n_retention": DxD_calves_f_n_retention,
                "DxD_calves_m_n_retention": DxD_calves_m_n_retention,
                "DxB_calves_f_n_retention": DxB_calves_f_n_retention,
                "DxB_calves_m_n_retention": DxB_calves_m_n_retention,
                "BxB_calves_m_n_retention": BxB_calves_m_n_retention,
                "BxB_calves_f_n_retention": BxB_calves_f_n_retention,
                "DxD_heifers_less_2_yr_n_retention": DxD_heifers_less_2_yr_n_retention,
                "DxD_steers_less_2_yr_n_retention": DxD_steers_less_2_yr_n_retention,
                "DxB_heifers_less_2_yr_n_retention": DxB_heifers_less_2_yr_n_retention,
                "DxB_steers_less_2_yr_n_retention": DxB_steers_less_2_yr_n_retention,
                "BxB_heifers_less_2_yr_n_retention": BxB_heifers_less_2_yr_n_retention,
                "BxB_steers_less_2_yr_n_retention": BxB_steers_less_2_yr_n_retention,
                "DxD_heifers_more_2_yr_n_retention": DxD_heifers_more_2_yr_n_retention,
                "DxD_steers_more_2_yr_n_retention": DxD_steers_more_2_yr_n_retention,
                "DxB_heifers_more_2_yr_n_retention": DxB_heifers_more_2_yr_n_retention,
                "DxB_steers_more_2_yr_n_retention": DxB_steers_more_2_yr_n_retention,
                "BxB_heifers_more_2_yr_n_retention": BxB_heifers_more_2_yr_n_retention,
                "BxB_steers_more_2_yr_n_retention": BxB_steers_more_2_yr_n_retention,
                "bulls_n_retention": bulls_n_retention,
            }

    def get_birth_weight(self):
        """
        Get the birth weight of the animals.

        Returns:
            float: The birth weight of the animals.
        """
        return self.animal_features.get("birth_weight")

    def get_mature_weight_bulls(self):
        """
        Get the mature weight of bulls.

        Returns:
            float: The mature weight of bulls.
        """
        return self.animal_features.get("mature_weight_bulls")

    def get_mature_weight_dairy_cows(self):
        """
        Get the mature weight of dairy cows.

        Returns:
            float: The mature weight of dairy cows.
        """
        return self.animal_features.get("mature_weight_dairy_cows")

    def get_mature_weight_suckler_cows(self):
        """
        Get the mature weight of suckler cows.

        Returns:
            float: The mature weight of suckler cows.
        """
        return self.animal_features.get("mature_weight_suckler_cows")

    def get_dairy_cows_weight_gain(self):
        """
        Get the weight gain of dairy cows.

        Returns:
            float: The weight gain of dairy cows.
        """
        return self.animal_features.get("dairy_cows_weight_gain")

    def get_suckler_cows_weight_gain(self):
        """
        Get the weight gain of suckler cows.

        Returns:
            float: The weight gain of suckler cows.
        """
        return self.animal_features.get("suckler_cows_weight_gain")

    def get_DxD_calves_m_weight_gain(self):
        """
        Get the weight gain of DxD male calves.

        Returns:
            float: The weight gain of dairy male calves.
        """
        return self.animal_features.get("DxD_calves_m_weight_gain")

    def get_DxD_calves_f_weight_gain(self):
        """
        Get the weight gain of DxD female calves.

        Returns:
            float: The weight gain of dairy female calves.
        """
        return self.animal_features.get("DxD_calves_f_weight_gain")

    def get_DxB_calves_m_weight_gain(self):
        """
        Get the weight gain of DxB male calves.

        Returns:
            float: The weight gain of dairy-beef male calves.
        """
        return self.animal_features.get("DxB_calves_m_weight_gain")

    def get_DxB_calves_f_weight_gain(self):
        """
        Get the weight gain of DxB female calves.

        Returns:
            float: The weight gain of dairy-beef female calves.
        """
        return self.animal_features.get("DxB_calves_f_weight_gain")

    def get_BxB_calves_m_weight_gain(self):
        """
        Get the weight gain of BxB male calves.

        Returns:
            float: The weight gain of suckler beef male calves.
        """
        return self.animal_features.get("BxB_calves_m_weight_gain")

    def get_BxB_calves_f_weight_gain(self):
        """
        Get the weight gain of BxB female calves.

        Returns:
            float: The weight gain of suckler beef female calves.
        """
        return self.animal_features.get("BxB_calves_f_weight_gain")

    def get_DxD_heifers_less_2_yr_weight_gain(self):
        """
        Get the weight gain of DxD heifers less than 2 years old.

        Returns:
            float: The weight gain of dairy heifers less than 2 years old.
        """
        return self.animal_features.get("DxD_heifers_less_2_yr_weight_gain")

    def get_DxD_steers_less_2_yr_weight_gain(self):
        """
        Get the weight gain of DxD steers less than 2 years old.

        Returns:
            float: The weight gain of dairy steers less than 2 years old.
        """
        return self.animal_features.get("DxD_steers_less_2_yr_weight_gain")

    def get_DxB_heifers_less_2_yr_weight_gain(self):
        """
        Get the weight gain of DxB heifers less than 2 years old.

        Returns:
            float: The weight gain of dairy-beef heifers less than 2 years old.
        """
        return self.animal_features.get("DxB_heifers_less_2_yr_weight_gain")

    def get_DxB_steers_less_2_yr_weight_gain(self):
        """
        Get the weight gain of DxB steers less than 2 years old.

        Returns:
            float: The weight gain of dairy-beef steers less than 2 years old.
        """
        return self.animal_features.get("DxB_steers_less_2_yr_weight_gain")

    def get_BxB_heifers_less_2_yr_weight_gain(self):
        """
        Get the weight gain of BxB heifers less than 2 years old.

        Returns:
            float: The weight gain of suckler beef heifers less than 2 years old.
        """
        return self.animal_features.get("BxB_heifers_less_2_yr_weight_gain")

    def get_BxB_steers_less_2_yr_weight_gain(self):
        """
        Get the weight gain of BxB steers less than 2 years old.

        Returns:
            float: The weight gain of suckler beef steers less than 2 years old.
        """
        return self.animal_features.get("BxB_steers_less_2_yr_weight_gain")

    def get_DxD_heifers_more_2_yr_weight_gain(self):
        """
        Get the weight gain of DxD heifers more than 2 years old.

        Returns:
            float: The weight gain of dairy heifers more than 2 years old.
        """
        return self.animal_features.get("DxD_heifers_more_2_yr_weight_gain")

    def get_DxD_steers_more_2_yr_weight_gain(self):
        """
        Get the weight gain of DxD steers more than 2 years old.

        Returns:
            float: The weight gain of dairy steers more than 2 years old.
        """
        return self.animal_features.get("DxD_steers_more_2_yr_weight_gain")

    def get_DxB_heifers_more_2_yr_weight_gain(self):
        """
        Get the weight gain of DxB heifers more than 2 years old.

        Returns:
            float: The weight gain of dairy-beef heifers more than 2 years old.
        """
        return self.animal_features.get("DxB_heifers_more_2_yr_weight_gain")

    def get_DxB_steers_more_2_yr_weight_gain(self):
        """
        Get the weight gain of DxB steers more than 2 years old.

        Returns:
            float: The weight gain of dairy-beef steers more than 2 years old.
        """
        return self.animal_features.get("DxB_steers_more_2_yr_weight_gain")

    def get_BxB_heifers_more_2_yr_weight_gain(self):
        """
        Get the weight gain of BxB heifers more than 2 years old.

        Returns:
            float: The weight gain of suckler beef heifers more than 2 years old.
        """
        return self.animal_features.get("BxB_heifers_more_2_yr_weight_gain")

    def get_BxB_steers_more_2_yr_weight_gain(self):
        """
        Get the weight gain of BxB steers more than 2 years old.

        Returns:
            float: The weight gain of suckler beef steers more than 2 years old.
        """
        return self.animal_features.get("BxB_steers_more_2_yr_weight_gain")

    def get_bulls_weight_gain(self):
        """
        Get the weight gain of bulls.

        Returns:
            float: The weight gain of bulls.
        """
        return self.animal_features.get("bulls_weight_gain")

    def get_dairy_cows_n_retention(self):
        """
        Get the nitrogen retention of dairy cows.

        Returns:
            float: The nitrogen retention of dairy cows.
        """
        return self.animal_features.get("dairy_cows_n_retention")

    def get_suckler_cows_n_retention(self):
        """
        Get the nitrogen retention of suckler cows.

        Returns:
            float: The nitrogen retention of suckler cows.
        """
        return self.animal_features.get("suckler_cows_n_retention")

    def get_DxD_calves_m_n_retention(self):
        """
        Get the nitrogen retention of DxD male calves

        Returns:
            float: The nitrogen retention of male dairy calves.
        """
        return self.animal_features.get("DxD_calves_m_n_retention")

    def get_DxD_calves_f_n_retention(self):
        """
        Get the nitrogen retention of DxD female calves.

        Returns:
            float: The nitrogen retention female dairy calves.
        """
        return self.animal_features.get("DxD_calves_f_n_retention")

    def get_DxB_calves_m_n_retention(self):
        """
        Get the nitrogen retention of DxB male calves.

        Returns:
            float: The nitrogen retention dairy-beef male calves.
        """
        return self.animal_features.get("DxB_calves_m_n_retention")

    def get_DxB_calves_f_n_retention(self):
        """
        Get the nitrogen retention of DxB female calves.

        Returns:
            float: The nitrogen retention dairy-beef female calves.
        """
        return self.animal_features.get("DxB_calves_f_n_retention")

    def get_BxB_calves_m_n_retention(self):
        """ 
        Get the nitrogen retention of BxB male calves.

        Returns:
            float: The nitrogen retention suckler beef male calves.
        """
        return self.animal_features.get("BxB_calves_m_n_retention")

    def get_BxB_calves_f_n_retention(self):
        """
        Get the nitrogen retention of BxB female calves.

        Returns:
            float: The nitrogen retention of suckler beef female calves.
        """
        return self.animal_features.get("BxB_calves_f_n_retention")

    def get_DxD_heifers_less_2_yr_n_retention(self):
        """
        Get the nitrogen retention of DxD heifers less than 2 years old.

        Returns:
            float: The nitrogen retention of dairy heifers less than 2 years old.
        """
        return self.animal_features.get("DxD_heifers_less_2_yr_n_retention")

    def get_DxD_steers_less_2_yr_n_retention(self):
        """
        Get the nitrogen retention of DxD steers less than 2 years old.

        Returns:
            float: The nitrogen retention of dairy steers less than 2 years old.
        """
        return self.animal_features.get("DxD_steers_less_2_yr_n_retention")

    def get_DxB_heifers_less_2_yr_n_retention(self):
        """
        Get the nitrogen retention of DxB heifers less than 2 years old.

        Returns:
            float: The nitrogen retention of dairy-beef heifers less than 2 years old.
        """
        return self.animal_features.get("DxB_heifers_less_2_yr_n_retention")

    def get_DxB_steers_less_2_yr_n_retention(self):#
        """
        Get the nitrogen retention of DxB steers less than 2 years old.

        Returns:
            float: The nitrogen retention of dairy-beef steers less than 2 years old.
        """
        return self.animal_features.get("DxB_steers_less_2_yr_n_retention")

    def get_BxB_heifers_less_2_yr_n_retention(self):
        """
        Get the nitrogen retention of BxB heifers less than 2 years old.

        Returns:
            float: The nitrogen retention of suckler beef heifers less than 2 years old.
        """
        return self.animal_features.get("BxB_heifers_less_2_yr_n_retention")

    def get_BxB_steers_less_2_yr_n_retention(self):
        """
        Get the nitrogen retention of BxB steers less than 2 years old.

        Returns:
            float: The nitrogen retention of suckler beef steers less than 2 years old.
        """
        return self.animal_features.get("BxB_steers_less_2_yr_n_retention")

    def get_DxD_heifers_more_2_yr_n_retention(self):
        """
        Get the nitrogen retention of DxD heifers more than 2 years old.

        Returns:
            float: The nitrogen retention of dairy heifers more than 2 years old.
        """
        return self.animal_features.get("DxD_heifers_more_2_yr_n_retention")

    def get_DxD_steers_more_2_yr_n_retention(self):
        """
        Get the nitrogen retention of DxD steers more than 2 years old.

        Returns:
            float: The nitrogen retention of dairy steers more than 2 years old.
        """
        return self.animal_features.get("DxD_steers_more_2_yr_n_retention")

    def get_DxB_heifers_more_2_yr_n_retention(self):
        """
        Get the nitrogen retention of DxB heifers more than 2 years old.

        Returns:
            float: The nitrogen retention of dairy-beef heifers more than 2 years old.
        """
        return self.animal_features.get("DxB_heifers_more_2_yr_n_retention")

    def get_DxB_steers_more_2_yr_n_retention(self):
        """
        Get the nitrogen retention of DxB steers more than 2 years old.

        Returns:
            float: The nitrogen retention of dairy-beef steers more than 2 years old.
        """
        return self.animal_features.get("DxB_steers_more_2_yr_n_retention")

    def get_BxB_heifers_more_2_yr_n_retention(self):
        """
        Get the nitrogen retention of BxB heifers more than 2 years old.

        Returns:
            float: The nitrogen retention of suckler beef heifers more than 2 years old.
        """
        return self.animal_features.get("BxB_heifers_more_2_yr_n_retention")

    def get_BxB_steers_more_2_yr_n_retention(self):
        """
        Get the nitrogen retention of BxB steers more than 2 years old.

        Returns:
            float: The nitrogen retention of suckler beef steers more than 2 years old.
        """
        return self.animal_features.get("BxB_steers_more_2_yr_n_retention")

    def get_bulls_n_retention(self):
        """
        Get the nitrogen retention of bulls.

        Returns:
            float: The nitrogen retention of bulls.
        """
        return self.animal_features.get("bulls_n_retention")

    def get_data(self):
        """
        Get the DataFrame containing the animal features data.

        Returns:
            pandas.DataFrame: The DataFrame containing the animal features data.
        """
        return self.data_frame

    def is_loaded(self):
        """
        Check if the animal features data has been successfully loaded.

        Returns:
            bool: True if the data has been loaded, False otherwise.
        """
        if self.data_frame is not None:
            return True
        else:
            return False


#######################################################################################


######################################################################################
# Emissions Factors Data
######################################################################################
class Emissions_Factors(object):
    """
    A class that encapsulates emissions factor data for various elements related to livestock farming. This includes 
    factors for methane production, nitrogen emissions, and energy use among others. The class provides methods to 
    retrieve specific emissions factors based on livestock types and activities.

    Attributes:
        data_frame (pandas.DataFrame): A DataFrame containing all the emissions factors data.
        emissions_factors (dict): A dictionary mapping emissions factor names to their values.

    Parameters:
        data (pandas.DataFrame): The DataFrame containing emissions factors data. Each row represents a different 
                                 set of factors and includes columns for each type of emissions factor.

    Methods:
        Each 'get' method corresponds to a specific type of emissions factor, allowing for easy retrieval of data 
        for use in calculations. For example, get_ef_net_energy_for_maintenance_non_lactating_cow() returns the 
        energy required for maintenance of non-lactating cows.

    """
    def __init__(self, data):
        self.data_frame = data

        self.emissions_factors = {}

        for _, row in self.data_frame.iterrows():
            ef_net_energy_for_maintenance_non_lactating_cow = row.get(
                "ef_net_energy_for_maintenance_non_lactating_cow"
            )
            ef_net_energy_for_maintenance_lactating_cow = row.get(
                "ef_net_energy_for_maintenance_lactating_cow"
            )
            ef_net_energy_for_maintenance_bulls = row.get(
                "ef_net_energy_for_maintenance_bulls"
            )
            ef_feeding_situation_pasture = row.get("ef_feeding_situation_pasture")
            ef_feeding_situation_large_area = row.get("ef_feeding_situation_large_area")
            ef_feeding_situation_stall = row.get("ef_feeding_situation_stall")
            ef_net_energy_for_growth_females = row.get(
                "ef_net_energy_for_growth_females"
            )
            ef_net_energy_for_growth_castrates = row.get(
                "ef_net_energy_for_growth_castrates"
            )
            ef_net_energy_for_growth_bulls = row.get("ef_net_energy_for_growth_bulls")
            ef_net_energy_for_pregnancy = row.get("ef_net_energy_for_pregnancy")
            ef_methane_conversion_factor_dairy_cow = row.get(
                "ef_methane_conversion_factor_dairy_cow"
            )
            ef_methane_conversion_factor_steer = row.get(
                "ef_methane_conversion_factor_steer"
            )
            ef_methane_conversion_factor_calves = row.get(
                "ef_methane_conversion_factor_calves"
            )
            ef_methane_conversion_factor_bulls = row.get(
                "ef_methane_conversion_factor_bulls"
            )
            ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition = row.get(
                "ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition"
            )
            ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o = row.get(
                "ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o"
            )
            ef_direct_n2o_emissions_soils = row.get("ef_direct_n2o_emissions_soils")
            ef_indirect_n2o_atmospheric_deposition_to_soils_and_water = row.get(
                "ef_indirect_n2o_atmospheric_deposition_to_soils_and_water"
            )
            ef_indirect_n2o_from_leaching_and_runoff = row.get(
                "ef_indirect_n2o_from_leaching_and_runoff"
            )
            ef_TAN_house_liquid = row.get("ef_TAN_house_liquid")
            ef_TAN_house_solid = row.get("ef_TAN_house_solid")
            ef_TAN_storage_tank = row.get("ef_TAN_storage_tank")
            ef_TAN_storage_solid = row.get("ef_TAN_storage_solid")
            ef_mcf_liquid_tank = row.get("ef_mcf_liquid_tank")
            ef_mcf_solid_storage = row.get("ef_mcf_solid_storage")
            ef_mcf_anaerobic_digestion = row.get("ef_mcf_anaerobic_digestion")
            ef_n2o_direct_storage_tank_liquid = row.get(
                "ef_n2o_direct_storage_tank_liquid"
            )
            ef_n2o_direct_storage_tank_solid = row.get(
                "ef_n2o_direct_storage_tank_solid"
            )
            ef_n2o_direct_storage_solid = row.get("ef_n2o_direct_storage_solid")
            ef_n2o_direct_storage_tank_anaerobic_digestion = row.get(
                "ef_n2o_direct_storage_tank_anaerobic_digestion"
            )
            ef_nh3_daily_spreading_none = row.get("ef_nh3_daily_spreading_none")
            ef_nh3_daily_spreading_manure = row.get("ef_nh3_daily_spreading_manure")
            ef_nh3_daily_spreading_broadcast = row.get(
                "ef_nh3_daily_spreading_broadcast"
            )
            ef_nh3_daily_spreading_injection = row.get(
                "ef_nh3_daily_spreading_injection"
            )
            ef_nh3_daily_spreading_traling_hose = row.get(
                "ef_nh3_daily_spreading_trailing_hose"
            )
            ef_urea = row.get("ef_urea")
            ef_urea_and_nbpt = row.get("ef_urea_and_nbpt")
            ef_fracGASF_urea_fertilisers_to_nh3_and_nox = row.get(
                "ef_fracGASF_urea_fertilisers_to_nh3_and_nox"
            )
            ef_fracGASF_urea_and_nbpt_to_nh3_and_nox = row.get(
                "ef_fracGASF_urea_and_nbpt_to_nh3_and_nox"
            )
            ef_frac_leach_runoff = row.get("ef_frac_leach_runoff")
            ef_ammonium_nitrate = row.get("ef_ammonium_nitrate")
            ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox = row.get(
                "ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox"
            )
            Frac_P_Leach = row.get("Frac_P_Leach")
            ef_urea_co2 = row.get("ef_urea_co2")
            ef_lime_co2 = row.get("ef_lime_co2")

            self.emissions_factors = {
                "ef_net_energy_for_maintenance_non_lactating_cow": ef_net_energy_for_maintenance_non_lactating_cow,
                "ef_net_energy_for_maintenance_lactating_cow": ef_net_energy_for_maintenance_lactating_cow,
                "ef_net_energy_for_maintenance_bulls": ef_net_energy_for_maintenance_bulls,
                "ef_feeding_situation_pasture": ef_feeding_situation_pasture,
                "ef_feeding_situation_large_area": ef_feeding_situation_large_area,
                "ef_feeding_situation_stall": ef_feeding_situation_stall,
                "ef_net_energy_for_growth_females": ef_net_energy_for_growth_females,
                "ef_net_energy_for_growth_castrates": ef_net_energy_for_growth_castrates,
                "ef_net_energy_for_growth_bulls": ef_net_energy_for_growth_bulls,
                "ef_net_energy_for_pregnancy": ef_net_energy_for_pregnancy,
                "ef_methane_conversion_factor_dairy_cow": ef_methane_conversion_factor_dairy_cow,
                "ef_methane_conversion_factor_steer": ef_methane_conversion_factor_steer,
                "ef_methane_conversion_factor_calves": ef_methane_conversion_factor_calves,
                "ef_methane_conversion_factor_bulls": ef_methane_conversion_factor_bulls,
                "ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition": ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o": ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "ef_direct_n2o_emissions_soils": ef_direct_n2o_emissions_soils,
                "ef_indirect_n2o_atmospheric_deposition_to_soils_and_water": ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "ef_indirect_n2o_from_leaching_and_runoff": ef_indirect_n2o_from_leaching_and_runoff,
                "ef_TAN_house_liquid": ef_TAN_house_liquid,
                "ef_TAN_house_solid": ef_TAN_house_solid,
                "ef_TAN_storage_tank": ef_TAN_storage_tank,
                "ef_TAN_storage_solid": ef_TAN_storage_solid,
                "ef_mcf_liquid_tank": ef_mcf_liquid_tank,
                "ef_mcf_solid_storage": ef_mcf_solid_storage,
                "ef_mcf_anaerobic_digestion": ef_mcf_anaerobic_digestion,
                "ef_n2o_direct_storage_tank_liquid": ef_n2o_direct_storage_tank_liquid,
                "ef_n2o_direct_storage_tank_solid": ef_n2o_direct_storage_tank_solid,
                "ef_n2o_direct_storage_solid": ef_n2o_direct_storage_solid,
                "ef_n2o_direct_storage_tank_anaerobic_digestion": ef_n2o_direct_storage_tank_anaerobic_digestion,
                "ef_nh3_daily_spreading_none": ef_nh3_daily_spreading_none,
                "ef_nh3_daily_spreading_manure": ef_nh3_daily_spreading_manure,
                "ef_nh3_daily_spreading_broadcast": ef_nh3_daily_spreading_broadcast,
                "ef_nh3_daily_spreading_injection": ef_nh3_daily_spreading_injection,
                "ef_nh3_daily_spreading_traling_hose": ef_nh3_daily_spreading_traling_hose,
                "ef_urea": ef_urea,
                "ef_urea_and_nbpt": ef_urea_and_nbpt,
                "ef_fracGASF_urea_fertilisers_to_nh3_and_nox": ef_fracGASF_urea_fertilisers_to_nh3_and_nox,
                "ef_fracGASF_urea_and_nbpt_to_nh3_and_nox": ef_fracGASF_urea_and_nbpt_to_nh3_and_nox,
                "ef_frac_leach_runoff": ef_frac_leach_runoff,
                "ef_ammonium_nitrate": ef_ammonium_nitrate,
                "ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox": ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox,
                "ef_Frac_P_Leach": Frac_P_Leach,
                "ef_urea_co2":ef_urea_co2,
                "ef_lime_co2":ef_lime_co2,
            }

    def get_ef_net_energy_for_maintenance_non_lactating_cow(self):
        """
        Get the net energy required for maintenance of non-lactating cows.

        Returns:
            float: The net energy required for maintenance of non-lactating cows.
        """
        return self.emissions_factors.get(
            "ef_net_energy_for_maintenance_non_lactating_cow"
        )

    def get_ef_net_energy_for_maintenance_lactating_cow(self):
        """
        Get the net energy required for maintenance of lactating cows.

        Returns:
            float: The net energy required for maintenance of lactating cows.
        """
        return self.emissions_factors.get("ef_net_energy_for_maintenance_lactating_cow")

    def get_ef_net_energy_for_maintenance_bulls(self):
        """
        Get the net energy required for maintenance of bulls.

        Returns:
            float: The net energy required for maintenance of bulls.
        """
        return self.emissions_factors.get("ef_net_energy_for_maintenance_bulls")

    def get_ef_feeding_situation_pasture(self):
        """
        Get the coefficient for feeding situations on pasture.

        Returns:
            float: The coefficient for feeding situations on pasture.
        """
        return self.emissions_factors.get("ef_feeding_situation_pasture")

    def get_ef_feeding_situation_large_area(self):
        """
        Get the coefficientfor feeding situations on large areas.

        Returns:
            float: The coefficient for feeding situations on large areas.
        """
        return self.emissions_factors.get("ef_feeding_situation_large_area")

    def get_ef_feeding_situation_stall(self):
        """
        Get the coefficient for feeding situations in stalls.

        Returns:
            float: The coefficient for feeding situations in stalls.
        """
        return self.emissions_factors.get("ef_feeding_situation_stall")

    def get_ef_net_energy_for_growth_females(self):
        """
        Get the net energy required for growth females.

        Returns:
            float: The net energy required for growth for females
        """
        return self.emissions_factors.get("ef_net_energy_for_growth_females")

    def get_ef_net_energy_for_growth_castrates(self):
        """
        Get the net energy required for growth of castrates.

        Returns:
            float: The net energy required for growth of castrates.
        """
        return self.emissions_factors.get("ef_net_energy_for_growth_castrates")

    def get_ef_net_energy_for_growth_bulls(self):
        """
        Get the net energy required for growth of bulls.

        Returns:
            float: The net energy required for growth of bulls.
        """
        return self.emissions_factors.get("ef_net_energy_for_growth_bulls")

    def get_ef_net_energy_for_pregnancy(self):
        """
        Get the net energy required for pregnancy.

        Returns:
            float: The net energy required for pregnancy.
        """
        return self.emissions_factors.get("ef_net_energy_for_pregnancy")

    def get_ef_methane_conversion_factor_dairy_cow(self):
        """
        Get the methane conversion factor for dairy cows.

        Returns:
            float: The methane conversion factor for dairy cows.
        """
        return self.emissions_factors.get("ef_methane_conversion_factor_dairy_cow")

    def get_ef_methane_conversion_factor_steer(self):
        """
        Get the methane conversion factor for steers.

        Returns:
            float: The methane conversion factor for steers.
        """
        return self.emissions_factors.get("ef_methane_conversion_factor_steer")

    def get_ef_methane_conversion_factor_calves(self):
        """
        Get the methane conversion factor for calves.

        Returns:
            float: The methane conversion factor for calves.
        """
        return self.emissions_factors.get("ef_methane_conversion_factor_calves")

    def get_ef_methane_conversion_factor_bulls(self):
        """
        Get the methane conversion factor for bulls.

        Returns:
            float: The methane conversion factor for bulls.
        """
        return self.emissions_factors.get("ef_methane_conversion_factor_bulls")

    def get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(self):
        """
        Get the emissions factor for total ammonia nitrogen pasture range paddock deposition.

        Returns:
            float: The emissions factor for total ammonia nitrogen pasture range paddock deposition.
        """
        return self.emissions_factors.get(
            "ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition"
        )

    def get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(self):
        """
        Get the emissions factor for pasture range paddock for dairy and non-dairy direct N2O.

        Returns:
            float: The emissions factor for pasture range paddock for dairy and non-dairy direct N2O.
        """
        return self.emissions_factors.get(
            "ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o"
        )

    def get_ef_direct_n2o_emissions_soils(self):
        """
        Get the emissions factor for direct N2O emissions from soils.

        Returns:
            float: The emissions factor for direct N2O emissions from soils.
        """
        return self.emissions_factors.get("ef_direct_n2o_emissions_soils")

    def get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(self):
        """
        Get the emissions factor for indirect N2O atmospheric deposition to soils and water.

        Returns:
            float: The emissions factor for indirect N2O atmospheric deposition to soils and water.
        """
        return self.emissions_factors.get(
            "ef_indirect_n2o_atmospheric_deposition_to_soils_and_water"
        )

    def get_ef_indirect_n2o_from_leaching_and_runoff(self):
        """
        Get the emissions factor for indirect N2O from leaching and runoff.

        Returns:
            float: The emissions factor for indirect N2O from leaching and runoff.
        """
        return self.emissions_factors.get("ef_indirect_n2o_from_leaching_and_runoff")

    def get_ef_TAN_house_liquid(self):
        """
        Get the emissions factor for TAN house liquid storage housing stage.

        Returns:
            float: The emissions factor for TAN house liquid storage housing stage.
        """
        return self.emissions_factors.get("ef_TAN_house_liquid")

    def get_ef_TAN_house_solid(self):
        """
        Get the emissions factor for TAN house solid storage housing stage.

        Returns:
            float: The emissions factor for TAN house solid storage housing stage.
        """
        return self.emissions_factors.get("ef_TAN_house_solid")

    def get_ef_TAN_storage_tank(self):
        """
        Get the emissions factor for TAN storage tank.

        Returns:
            float: The emissions factor for TAN storage tank.
        """
        return self.emissions_factors.get("ef_TAN_storage_tank")

    def get_ef_TAN_storage_solid(self):
        """
        Get the emissions factor for TAN storage solid.

        Returns:
            float: The emissions factor for TAN storage solid.
        """
        return self.emissions_factors.get("ef_TAN_storage_solid")

    def get_ef_mcf_liquid_tank(self):
        """
        Get the emissions factor for MCF liquid tank.

        Returns:
            float: The emissions factor for MCF liquid tank.
        """
        return self.emissions_factors.get("ef_mcf_liquid_tank")

    def get_ef_mcf_solid_storage(self):
        """
        Get the emissions factor for MCF solid storage.

        Returns:
            float: The emissions factor for MCF solid storage.
        """
        return self.emissions_factors.get("ef_mcf_solid_storage")

    def get_ef_mcf_anaerobic_digestion(self):
        """
        Get the emissions factor for MCF anaerobic digestion.

        Returns:
            float: The emissions factor for MCF anaerobic digestion.
        """
        return self.emissions_factors.get("ef_mcf_anaerobic_digestion")

    def get_ef_n2o_direct_storage_tank_liquid(self):
        """
        Get the emissions factor for N2O direct storage tank liquid.

        Returns:
            float: The emissions factor for N2O direct storage tank liquid.
        """
        return self.emissions_factors.get("ef_n2o_direct_storage_tank_liquid")

    def get_ef_n2o_direct_storage_tank_solid(self):
        """
        Get the emissions factor for N2O direct storage tank solid.

        Returns:
            float: The emissions factor for N2O direct storage tank solid.
        """
        return self.emissions_factors.get("ef_n2o_direct_storage_tank_solid")

    def get_ef_n2o_direct_storage_solid(self):
        """
        Get the emissions factor for N2O direct storage solid.

        Returns:
            float: The emissions factor for N2O direct storage solid.
        """
        return self.emissions_factors.get("ef_n2o_direct_storage_solid")

    def get_ef_n2o_direct_storage_tank_anaerobic_digestion(self):
        """
        Get the emissions factor for N2O direct storage tank anaerobic digestion.
        
        Returns:
            float: The emissions factor for N2O direct storage tank anaerobic digestion.
        """
        return self.emissions_factors.get(
            "ef_n2o_direct_storage_tank_anaerobic_digestion"
        )

    def get_ef_nh3_daily_spreading_none(self):
        """
        Get the emissions factor for NH3 daily spreading none.

        Returns:
            float: The emissions factor for NH3 daily spreading none.
        """
        return self.emissions_factors.get("ef_nh3_daily_spreading_none")

    def get_ef_nh3_daily_spreading_manure(self):
        """
        Get the emissions factor for NH3 daily spreading manure.

        Returns:
            float: The emissions factor for NH3 daily spreading manure.
        """
        return self.emissions_factors.get("ef_nh3_daily_spreading_manure")

    def get_ef_nh3_daily_spreading_broadcast(self):
        """
        Get the emissions factor for NH3 daily spreading broadcast.

        Returns:
            float: The emissions factor for NH3 daily spreading broadcast.
        """
        return self.emissions_factors.get("ef_nh3_daily_spreading_broadcast")

    def get_ef_nh3_daily_spreading_injection(self):
        """
        Get the emissions factor for NH3 daily spreading injection.

        Returns:
            float: The emissions factor for NH3 daily spreading injection.
        """
        return self.emissions_factors.get("ef_nh3_daily_spreading_injection")

    def get_ef_nh3_daily_spreading_traling_hose(self):
        """
        Get the emissions factor for NH3 daily spreading trailing hose.

        Returns:
            float: The emissions factor for NH3 daily spreading trailing hose.
        """
        return self.emissions_factors.get("ef_nh3_daily_spreading_traling_hose")

    def get_ef_urea(self):
        """
        Get the emissions factor for urea.

        Returns:
            float: The emissions factor for urea.
        """
        return self.emissions_factors.get("ef_urea")

    def get_ef_urea_and_nbpt(self):
        """
        Get the emissions factor for urea and NBPT.

        Returns:
            float: The emissions factor for urea and NBPT.
        """
        return self.emissions_factors.get("ef_urea_and_nbpt")

    def get_ef_fracGASF_urea_fertilisers_to_nh3_and_nox(self):
        """
        Get the emissions factor for urea fertilisers to NH3 and NOx.

        Returns:
            float: The emissions factor for urea fertilisers to NH3 and NOx.
        """
        return self.emissions_factors.get("ef_fracGASF_urea_fertilisers_to_nh3_and_nox")

    def get_ef_fracGASF_urea_and_nbpt_to_nh3_and_nox(self):
        """
        Get the emissions factor for urea and NBPT to NH3 and NOx.

        Returns:
            float: The emissions factor for urea and NBPT to NH3 and NOx.
        """
        return self.emissions_factors.get("ef_fracGASF_urea_and_nbpt_to_nh3_and_nox")

    def get_ef_frac_leach_runoff(self):
        """
        Get the fraction of leaching and runoff.

        Returns:
            float: The fraction of leaching and runoff.
        """
        return self.emissions_factors.get("ef_frac_leach_runoff")

    def get_ef_ammonium_nitrate(self):
        """
        Get the emissions factor for ammonium nitrate.

        Returns:
            float: The emissions factor for ammonium nitrate.
        """
        return self.emissions_factors.get("ef_ammonium_nitrate")

    def get_ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox(self):
        """
        Get the emissions factor for ammonium fertilisers to NH3 and NOx.

        Returns:
            float: The emissions factor for ammonium fertilisers to NH3 and NOx.
        """
        return self.emissions_factors.get(
            "ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox"
        )

    def get_ef_Frac_P_Leach(self):
        """
        Get the fraction of phosphorus leaching.

        Returns:
            float: The fraction of phosphorus leaching.
        """
        return self.emissions_factors.get("ef_Frac_P_Leach")
    
    def get_ef_urea_co2(self):
        """
        Get the co2 emissions factor for urea.

        Returns:
            float: The co2 emissions factor for urea.
        """
        return self.emissions_factors.get("ef_urea_co2")
    
    def get_ef_lime_co2(self):
        """
        Get the co2 emissions factor for lime.

        Returns:
            float: The co2 emissions factor for lime.
        """
        return self.emissions_factors.get("ef_lime_co2")

    def get_data(self):
        """
        Get the DataFrame containing the emissions factors data.

        Returns:
            pandas.DataFrame: The DataFrame containing the emissions factors data.
        """
        return self.data_frame

    def is_loaded(self):
        """
        Check if the emissions factors data has been successfully loaded.

        Returns:
            bool: True if the data has been loaded, False otherwise.
        """
        if self.data_frame is not None:
            return True
        else:
            return False


#######################################################################################


class Grass(object):
    """
    Represents the data and functionality related to various types of grass.

    Attributes:
        data_frame (pandas.DataFrame): A DataFrame containing grass data.
        grasses (dict): A dictionary storing information for each grass genus, 
                        including its forage dry matter digestibility, crude protein, 
                        and gross energy values.

    Methods:
        average(property): Calculates the average value of a specified property 
                           (e.g., dry matter digestibility) across all grasses.
        get_forage_dry_matter_digestibility(forage): Returns the dry matter 
                                                      digestibility for a given forage.
        get_crude_protein(forage): Returns the crude protein value for a given forage.
        get_gross_energy_mje_dry_matter(forage): Returns the gross energy (in MJ per 
                                                 dry matter) for a given forage.
        get_data(): Returns the original data frame used to create the instance.
        is_loaded(): Checks whether the data frame is loaded successfully.
    """
    def average(self, property):
        values = [
            row.get(property)
            for _, row in self.data_frame.iterrows()
            if pandas.notna(row.get(property))
        ]

        return sum(values) / len(values)

    def __init__(self, data):
        self.data_frame = data

        self.grasses = {}

        for _, row in self.data_frame.iterrows():
            genus = row.get("grass_genus".lower())
            dmd = row.get("forage_dry_matter_digestibility")
            cp = row.get("crude_protein")
            ge = row.get("gross_energy")

            self.grasses[genus] = {
                "forage_dry_matter_digestibility": dmd,
                "crude_protein": cp,
                "gross_energy": ge,
            }

        # Pre-compute averages
        self.grasses["average"] = {
            "forage_dry_matter_digestibility": self.average(
                "forage_dry_matter_digestibility"
            ),
            "crude_protein": self.average("crude_protein"),
            "gross_energy": self.average("gross_energy"),
        }

    def get_forage_dry_matter_digestibility(self, forage):
        """
        Get the dry matter digestibility for a given forage.

        Args:
            forage (str): The name of the forage.

        Returns:
            float: The dry matter digestibility for the specified forage.
        """
        return self.grasses.get(forage).get("forage_dry_matter_digestibility")

    def get_crude_protein(self, forage):
        """
        Get the crude protein value for a given forage.

        Args:
            forage (str): The name of the forage.

        Returns:
            float: The crude protein value for the specified forage.
        """
        return self.grasses.get(forage).get("crude_protein")

    def get_gross_energy_mje_dry_matter(self, forage):
        """
        Get the gross energy (in MJ per dry matter) for a given forage.

        Args:
            forage (str): The name of the forage.

        Returns:
            float: The gross energy for the specified forage.
        """
        return self.grasses.get(forage).get("gross_energy")

    def get_data(self):
        """
        Get the DataFrame containing the grass data.

        Returns:
            pandas.DataFrame: The DataFrame containing the grass data.
        """
        return self.data_frame

    def is_loaded(self):
        """
        Check if the grass data has been successfully loaded.

        Returns:
            bool: True if the data has been loaded, False otherwise.
        """
        if self.data_frame is not None:
            return True
        else:
            return False


#######################################################################################
# concentrate file class
########################################################################################
class Concentrate(object):
    """
    Represents the data and functionality related to various types of animal feed concentrates.

    Attributes:
        data_frame (pandas.DataFrame): A DataFrame containing concentrate data.
        concentrates (dict): A dictionary storing information for each type of concentrate,
                             including its dry matter digestibility, digestible energy, crude protein,
                             gross energy, CO2 equivalents, and PO4 equivalents.

    Methods:
        average(property): Calculates the average value of a specified property (e.g., dry matter digestibility)
                           across all concentrates.
        get_con_dry_matter_digestibility(concentrate): Returns the dry matter digestibility for a given concentrate.
        get_con_digestible_energy(concentrate): Returns the digestible energy proportion for a given concentrate.
        get_con_crude_protein(concentrate): Returns the crude protein value for a given concentrate.
        get_gross_energy_mje_dry_matter(concentrate): Returns the gross energy (in MJ per dry matter) for a given concentrate.
        get_con_co2_e(concentrate): Returns the CO2 equivalents for a given concentrate.
        get_con_po4_e(concentrate): Returns the PO4 equivalents for a given concentrate.
        get_data(): Returns the original data frame used to create the instance.
        is_loaded(): Checks whether the data frame is loaded successfully.
    """
    def average(self, property):
        values = [
            row.get(property)
            for _, row in self.data_frame.iterrows()
            if pandas.notna(row.get(property))
        ]

        try:
            return sum(values) / len(values)
        except ZeroDivisionError as err:
            pass

    def __init__(self, data):
        self.data_frame = data

        self.concentrates = {}

        for _, row in self.data_frame.iterrows():
            con_type = row.get("con_type".lower())
            con_dmd = row.get("con_dry_matter_digestibility")
            con_de = row.get("con_digestible_energy")
            con_cp = row.get("con_crude_protein")
            con_gross_energy = row.get("gross_energy_mje_dry_matter")
            con_co2_e = row.get("con_co2_e")
            con_po4_e = row.get("con_po4_e")

            self.concentrates[con_type] = {
                "con_dry_matter_digestibility": con_dmd,
                "con_digestible_energy": con_de,
                "con_crude_protein": con_cp,
                "gross_energy_mje_dry_matter": con_gross_energy,
                "con_co2_e": con_co2_e,
                "con_po4_e": con_po4_e,
            }

        # Pre-compute averages
        self.concentrates["average"] = {
            "con_dry_matter_digestibility": self.average(
                "con_dry_matter_digestibility"
            ),
            "con_digestible_energy": self.average("con_digestible_energy"),
            "con_crude_protein": self.average("con_crude_protein"),
        }

    def get_con_dry_matter_digestibility(self, concentrate):
        """
        Get the dry matter digestibility for a given concentrate.

        Args:
            concentrate (str): The name of the concentrate.

        Returns:
            float: The dry matter digestibility for the specified concentrate.
        """
        return self.concentrates.get(concentrate).get("con_dry_matter_digestibility")

    def get_con_digestible_energy(self, concentrate):
        """
        Get the digestible energy proportion for a given concentrate.

        Args:
            concentrate (str): The name of the concentrate.

        Returns:
            float: The digestible energy proportion for the specified concentrate.
        """
        return self.concentrates.get(concentrate).get("con_digestible_energy")

    def get_con_crude_protein(self, concentrate):
        """
        Get the crude protein value for a given concentrate.

        Args:
            concentrate (str): The name of the concentrate.

        Returns:
            float: The crude protein value for the specified concentrate.
        """
        return self.concentrates.get(concentrate).get("con_crude_protein")

    def get_gross_energy_mje_dry_matter(self, concentrate):
        """
        Get the gross energy (in MJ per dry matter) for a given concentrate.

        Args:
            concentrate (str): The name of the concentrate.
            
        Returns:
            float: The gross energy for the specified concentrate.
        """
        return self.concentrates.get(concentrate).get("gross_energy_mje_dry_matter")

    def get_con_co2_e(self, concentrate):
        """
        Get the CO2 equivalents for a given concentrate.

        Args:
            concentrate (str): The name of the concentrate.

        Returns:
            float: The CO2 equivalents for the specified concentrate.
        """
        return self.concentrates.get(concentrate).get("con_co2_e")

    def get_con_po4_e(self, concentrate):
        """
        Get the PO4 equivalents for a given concentrate.

        Args:
            concentrate (str): The name of the concentrate.

        Returns:
            float: The PO4 equivalents for the specified concentrate.
        """
        return self.concentrates.get(concentrate).get("con_po4_e")

    def get_data(self):
        """
        Get the DataFrame containing the concentrate data.

        Returns:
            pandas.DataFrame: The DataFrame containing the concentrate data.
        """
        return self.data_frame

    def is_loaded(self):
        """
        Check if the concentrate data has been successfully loaded.

        Returns:
            bool: True if the data has been loaded, False otherwise.
        """
        if self.data_frame is not None:
            return True
        else:
            return False


########################################################################################
# Upstream class
########################################################################################
class Upstream(object):
    """
    Represents upstream data for various inputs in an agricultural context.

    Attributes:
        data_frame (pandas.DataFrame): A DataFrame containing upstream data.
        upstream (dict): A dictionary storing upstream data for each type, 
                         including functional units, CO2 equivalents, PO4 equivalents, 
                         SO2 equivalents, net calorific value, and antimony equivalents.

    Methods:
        get_upstream_fu(upstream): Returns the functional unit for a given upstream type.
        get_upstream_kg_co2e(upstream): Returns the kg of CO2 equivalents for a given upstream type.
        get_upstream_kg_po4e(upstream): Returns the kg of PO4 equivalents for a given upstream type.
        get_upstream_kg_so2e(upstream): Returns the kg of SO2 equivalents for a given upstream type.
        get_upstream_mje(upstream): Returns net calorific value in MJ for a given upstream type.
        get_upstream_kg_sbe(upstream): Returns the kg of antimony equivalents for a given upstream type.
        get_data(): Returns the original data frame from which the upstream data is derived.
        is_loaded(): Checks whether the data frame is loaded successfully.
    """
    def __init__(self, data):
        self.data_frame = data

        self.upstream = {}

        for _, row in self.data_frame.iterrows():
            upstream_type = row.get("upstream_type".lower())
            upstream_fu = row.get("upstream_fu")
            upstream_kg_co2e = row.get("upstream_kg_co2e")
            upstream_kg_po4e = row.get("upstream_kg_po4e")
            upstream_kg_so2e = row.get("upstream_kg_so2e")
            upstream_mje = row.get("upstream_mje")
            upstream_kg_sbe = row.get("upstream_kg_sbe")

            self.upstream[upstream_type] = {
                "upstream_fu": upstream_fu,
                "upstream_kg_co2e": upstream_kg_co2e,
                "upstream_kg_po4e": upstream_kg_po4e,
                "upstream_kg_so2e": upstream_kg_so2e,
                "upstream_mje": upstream_mje,
                "upstream_kg_sbe": upstream_kg_sbe,
            }

    def get_upstream_fu(self, upstream):
        """
        Get the functional unit for a given upstream type.

        Args:
            upstream (str): The name of the upstream type.

        Returns:
            float: The functional unit for the specified upstream type.
        """
        return self.upstream.get(upstream).get("upstream_fu")

    def get_upstream_kg_co2e(self, upstream):
        """
        Get the kg of CO2 equivalents for a given upstream type.

        Args:
            upstream (str): The name of the upstream type.

        Returns:
            float: The kg of CO2 equivalents for the specified upstream type.
        """
        return self.upstream.get(upstream).get("upstream_kg_co2e")

    def get_upstream_kg_po4e(self, upstream):
        """
        Get the kg of PO4 equivalents for a given upstream type.

        Args:
            upstream (str): The name of the upstream type.

        Returns:
            float: The kg of PO4 equivalents for the specified upstream type.
        """
        return self.upstream.get(upstream).get("upstream_kg_po4e")

    def get_upstream_kg_so2e(self, upstream):
        """
        Get the kg of SO2 equivalents for a given upstream type.

        Args:
            upstream (str): The name of the upstream type.

        Returns:
            float: The kg of SO2 equivalents for the specified upstream type.
        """
        return self.upstream.get(upstream).get("upstream_kg_so2e")

    def get_upstream_mje(self, upstream):
        """
        Get the net calorific value in MJ for a given upstream type.

        Args:
            upstream (str): The name of the upstream type.

        Returns:
            float: The net calorific value in MJ for the specified upstream type.
        """
        return self.upstream.get(upstream).get("upstream_mje")

    def get_upstream_kg_sbe(self, upstream):
        """
        Get the kg of antimony equivalents for a given upstream type.

        Args:
            upstream (str): The name of the upstream type.

        Returns:
            float: The kg of antimony equivalents for the specified upstream type.
        """
        return self.upstream.get(upstream).get("upstream_kg_sbe")

    def get_data(self):
        """
        Get the DataFrame containing the upstream data.

        Returns:
            pandas.DataFrame: The DataFrame containing the upstream data.
        """
        return self.data_frame

    def is_loaded(self):
        """
        Check if the upstream data has been successfully loaded.

        Returns:
            bool: True if the data has been loaded, False otherwise.
        """
        if self.data_frame is not None:
            return True
        else:
            return False


#############################################################################################


def load_grass_data():
    """
    Load the grass data.

    Returns:
        Grass: An instance of the Grass class containing the grass data.
    """
    return Grass()


def load_concentrate_data():
    """
    Load the concentrate data.

    Returns:
        Concentrate: An instance of the Concentrate class containing the concentrate data.
    """
    return Concentrate()


def load_upstream_data():
    """
    Load the upstream data.

    Returns:
        Upstream: An instance of the Upstream class containing the upstream data.
    """
    return Upstream()


def load_emissions_factors_data():
    """
    Load the emissions factors data.

    Returns:
        EmissionsFactors: An instance of the EmissionsFactors class containing the emissions factors data.
    """
    return Emissions_Factors()


def load_animal_features_data():
    """
    Load the animal features data.

    Returns:
        AnimalFeatures: An instance of the AnimalFeatures class containing the animal features data.
    """
    return Animal_Features()


def load_farm_data(farm_data_frame):
    """
    Load the farm data.

    Args:
        farm_data_frame (pandas.DataFrame): The DataFrame containing the farm data.

    Returns:
        dict: A dictionary containing the farm data.
    """
    scenario_list = []

    for _, row in farm_data_frame.iterrows():
        data = dict([(x, row.get(x)) for x in row.keys()])
        scenario_list.append(Farm(data))

    return dict(enumerate(scenario_list))


def load_livestock_data(animal_data_frame):
    """
    Load the livestock data.

    Args:
        animal_data_frame (pandas.DataFrame): The DataFrame containing the livestock data.

    Returns:
        dict: A dictionary containing the livestock data.
    """
    # 1. Load each animal category into an object

    categories = []

    for _, row in animal_data_frame.iterrows():
        data = dict([(x, row.get(x)) for x in row.keys()])
        categories.append(AnimalCategory(data))

    # 2. Aggregate the animal categories into collection based on the farm ID

    collections = {}

    for category in categories:
        farm_id = category.farm_id
        cohort = category.cohort

        if farm_id not in collections:
            collections[farm_id] = {cohort: category}
        else:
            collections[farm_id][cohort] = category

    # 3. Convert the raw collection data into animal collection objects

    collection_objects = {}

    for farm_id, raw_data in collections.items():
        collection_objects[farm_id] = {"animals": AnimalCollection(raw_data)}

    return collection_objects


def print_livestock_data(data):
    """
    Print the livestock data.

    Args:
        data (dict): A dictionary containing the livestock data.
    """
    for _, key in enumerate(data):
        for animal in data[key].keys():
            for cohort in data[key][animal].__dict__.keys():
                for attribute in (
                    data[key][animal].__getattribute__(cohort).__dict__.keys()
                ):
                    print(
                        f"{cohort}: {attribute} = {data[key][animal].__getattribute__(cohort).__getattribute__(attribute)}"
                    )


