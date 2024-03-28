"""
Animal data module
------------------
This module provides a class that contains static methods to access various attributes related to an animal's characteristics and management 
practices within a farming operation.
"""
class AnimalData:
    """
    The AnimalData class provides static methods to access various attributes related to an animal's characteristics and management practices 
    within a farming operation. This class is designed to facilitate the extraction of specific data from animal objects, 
    supporting calculations and analyses in environmental assessments, nutritional planning, and other agricultural applications.

    Each method in this class is a static method, meaning it can be called without creating an instance of the class. 
    These methods are intended to work with animal objects that contain attributes such as concentrate amount, forage type, cohort, and more.

    Methods:
        get_animal_concentrate_amount(animal): Returns the amount of concentrate feed consumed by the animal.
        get_animal_concentrate_type(animal): Returns the type of concentrate feed consumed by the animal.
        get_animal_forage(animal): Returns the type of forage consumed by the animal.
        get_animal_cohort(animal): Returns the cohort category to which the animal belongs.
        get_animal_population(animal): Returns the population count of the animal's group.
        get_animal_weight(animal): Returns the weight of the animal.
        get_animal_daily_milk(animal): Returns the daily milk yield of the animal, if applicable.
        get_animal_year(animal): Returns the year associated with the animal data.
        get_animal_grazing(animal): Returns the grazing management practice for the animal.
        get_animal_t_outdoors(animal): Returns the time spent outdoors by the animal.
        get_animal_t_indoors(animal): Returns the time spent indoors by the animal.
        get_animal_sold(animal): Returns the number of animals sold from this group.
        get_animal_bought(animal): Returns the number of animals bought into this group.
        get_animal_t_stabled(animal): Returns the time the animal is stabled.
        get_animal_mm_storage(animal): Returns the manure management storage type used for the animal.
        get_animal_daily_spreading(animal): Returns the type of daily spreading practice used for manure management.
        get_animal_wool(animal): Returns the amount of wool produced by the animal, if applicable.
        get_animal_ef_country(animal): Returns the country for which environmental factor data should be used.
        get_animal_farm_id(animal): Returns the identification number of the farm where the animal is raised.
    """
    @staticmethod
    def get_animal_concentrate_amount(animal):
        """
        Returns the amount of concentrate feed consumed by the animal.

        Parameters:
            animal (object): An animal object containing data attributes.

        Returns:
            float: The amount of concentrate feed consumed by the animal.
        """
        return animal.con_amount
    
    @staticmethod
    def get_animal_concentrate_type(animal):
        """
        Returns the type of concentrate feed consumed by the animal.

        Parameters:
            animal (object): An animal object containing data attributes.

        Returns:
            str: The type of concentrate feed consumed by the animal.
        """
        return animal.con_type
    
    @staticmethod
    def get_animal_forage(animal):
        """
        Returns the type of forage consumed by the animal.

        Parameters:
            animal (object): An animal object containing data attributes.

        Returns:
            str: The type of forage consumed by the animal.
        """
        return animal.forage
    
    @staticmethod
    def get_animal_cohort(animal):
        """
        Returns the cohort category to which the animal belongs.

        Parameters:
            animal (object): An animal object containing data attributes.

        Returns:
            str: The cohort category to which the animal belongs.
        """
        return animal.cohort
    
    @staticmethod
    def get_animal_population(animal):
        """
        Returns the population count of the animal's group.

        Parameters:
            animal (object): An animal object containing data attributes.

        Returns:
            float: The population count of the animal's group.
        """
        return animal.pop
    
    @staticmethod
    def get_animal_weight(animal):
        """
        Returns the weight of the animal.

        Parameters:
            animal (object): An animal object containing data attributes.

        Returns:
            float: The weight of the animal.
        """
        return animal.weight
    
    @staticmethod
    def get_animal_daily_milk(animal):
        """
        Returns the daily milk yield of the animal.

        Parameters:
            animal (object): An animal object containing data attributes.

        Returns:
            float: The daily milk yield of the animal.
        """
        return animal.daily_milk
    
    @staticmethod
    def get_animal_year(animal):
        """
        Returns the year associated with the animal data.

        Parameters:
            animal (object): An animal object containing data attributes.

        Returns:
            int: The year associated with the animal data.
        """
        return animal.year
    
    @staticmethod
    def get_animal_grazing(animal):
        """
        Returns the grazing management practice for the animal.

        Parameters:
            animal (object): An animal object containing data attributes.

        Returns:
            str: The grazing management practice for the animal.
        """
        return animal.grazing
    
    @staticmethod
    def get_animal_t_outdoors(animal):
        """
        Returns the time spent outdoors by the animal.

        Parameters:
            animal (object): An animal object containing data attributes.

        Returns:
            float: The time spent outdoors by the animal.
        """
        return animal.t_outdoors
    
    @staticmethod
    def get_animal_t_indoors(animal):
        """
        Returns the time spent indoors by the animal.

        Parameters:
            animal (object): An animal object containing data attributes.

        Returns:
            float: The time spent indoors by the animal.
        """
        return animal.t_indoors
    
    @staticmethod
    def get_animal_sold(animal):
        """
        Returns the number of animals sold from this group.

        Parameters:
            animal (object): An animal object containing data attributes.

        Returns:
            int: The number of animals sold from this group.
        """
        return animal.n_sold
    
    @staticmethod
    def get_animal_bought(animal):
        """
        Returns the number of animals bought into this group.

        Parameters:
            animal (object): An animal object containing data attributes.   

        Returns:
            int: The number of animals bought into this group.
        """
        return animal.n_bought
    
    @staticmethod
    def get_animal_t_stabled(animal):
        """
        Returns the time the animal is stabled.

        Parameters:
            animal (object): An animal object containing data attributes.

        Returns:
            float: The time the animal is stabled.
        """
        return animal.t_stabled
    
    @staticmethod
    def get_animal_mm_storage(animal):
        """
        Returns the manure management storage type used for the animal.

        Parameters:
            animal (object): An animal object containing data attributes.

        Returns:
            str: The manure management storage type used for the animal.
        """
        return animal.mm_storage
    
    @staticmethod
    def get_animal_daily_spreading(animal):
        """
        Returns the type of daily spreading

        Parameters:
            animal (object): An animal object containing data attributes.   

        Returns:
            float: The type of daily spreading practice used for manure management.
        """
        return animal.daily_spreading
    
    @staticmethod
    def get_animal_wool(animal):
        """
        Returns the amount of wool produced by the animal.

        Not Apllicable for all animals

        Parameters:
            animal (object): An animal object containing data attributes.

        Returns:
            float: The amount of wool produced by the animal.
        """
        return animal.wool
    
    @staticmethod
    def get_animal_ef_country(animal):
        """
        Returns the country for which environmental factor data should be used.

        Parameters:
            animal (object): An animal object containing data attributes.

        Returns:
            str: The country for which environmental factor data should be used.
        """
        return animal.ef_country
    
    @staticmethod
    def get_animal_farm_id(animal):
        """
        Returns the identification number.

        Parameters:
            animal (object): An animal object containing data attributes.

        Returns:
            int: The identification number.
        """
        return animal.farm_id
    