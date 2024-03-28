"""
Database Manager Module
-----------------------

This module contains the DataManager class, which is responsible for handling the retrieval of country-specific and generic data 
from the SQL database for use in lifecycle assessment calculations.
"""
import sqlalchemy as sqa
import pandas as pd
from cattle_lca.database import get_local_dir
import os


class DataManager:
    """
    DataManager handles the retrieval of country-specific and generic data from the SQL database for use in lifecycle assessment calculations. 
    It utilizes SQLAlchemy for database connection and operations. 
    The data is returned as Pandas DataFrames for easy manipulation and access within the Python ecosystem.

    Attributes:
        database_dir (str): Directory where the SQL database is stored.
        engine (sqa.engine.Engine): SQLAlchemy engine instance for connecting to the database.
        ef_country (str): The country identifier used to retrieve country-specific data.

    Args:
        ef_country (str): A string representing the country for which the data is to be loaded. It is used to filter the data in country-specific tables.

    Methods:
        data_engine_creater(): Initializes and returns a SQLAlchemy engine connected to the local cattle LCA database.
        grass_data(index=None): Retrieves grass-related data from the database. Optional index parameter sets a column as DataFrame index.
        upstream_data(index=None): Retrieves upstream (pre-farm gate inputs and processes) data. Optional index parameter for DataFrame indexing.
        emissions_factor_data(index=None): Fetches emissions factors specific to the set country. Can set an index column if provided.
        concentrate_data(index=None): Gathers data regarding animal feed concentrates. Optional indexing with the index parameter.
        animal_features_data(index=None): Collects data related to the features of various animal types, filtered by country. Indexing option available.
    """
    def __init__(self, ef_country):
        self.database_dir = get_local_dir()
        self.engine = self.data_engine_creater()
        self.ef_country = ef_country


    def data_engine_creater(self):
        """
        Initializes and returns a SQLAlchemy engine connected to the local cattle LCA database.

        Returns:
            sqa.engine.Engine: SQLAlchemy engine instance for connecting to the database.
        """
        database_path = os.path.abspath(
            os.path.join(self.database_dir, "cattle_database.db")
        )
        engine_url = f"sqlite:///{database_path}"

        return sqa.create_engine(engine_url)


    def grass_data(self, index=None):
        """
        Retrieves grass-related data from the database. Optional index parameter sets a column as DataFrame index.

        Args:
            index (str): The column to use as the DataFrame index.

        Returns:
            pd.DataFrame: A DataFrame containing grass-related data.
        """
        table = "grass_database"

        if index == None:
            dataframe = pd.read_sql("SELECT * FROM '%s'" % (table), self.engine)

        else:
            dataframe = pd.read_sql(
                "SELECT * FROM '%s'" % (table),
                self.engine,
                index_col=[index],
            )

        return dataframe


    def upstream_data(self, index=None):
        """
        Retrieves upstream (pre-farm gate inputs and processes) data. Optional index parameter for DataFrame indexing.

        Args:
            index (str): The column to use as the DataFrame index.

        Returns:
            pd.DataFrame: A DataFrame containing upstream data.
        """
        table = "upstream_database"

        if index == None:
            dataframe = pd.read_sql("SELECT * FROM '%s'" % (table), self.engine)

        else:
            dataframe = pd.read_sql(
                "SELECT * FROM '%s'" % (table),
                self.engine,
                index_col=[index],
            )

        return dataframe

    def emissions_factor_data(self, index=None):
        """
        Fetches emissions factors specific to the set country. Can set an index column if provided.

        Args:
            index (str): The column to use as the DataFrame index.

        Returns:
            pd.DataFrame: A DataFrame containing emissions factors data.
        """
        table = "emissions_factors_database"

        if index == None:
            dataframe = pd.read_sql(
                "SELECT * FROM '%s' WHERE ef_country = '%s'" % (table, self.ef_country),
                self.engine,
            )

        else:
            dataframe = pd.read_sql(
                "SELECT * FROM '%s' WHERE ef_country = '%s'" % (table, self.ef_country),
                self.engine,
                index_col=[index],
            )

        return dataframe
    

    def concentrate_data(self, index=None):
        """
        Gathers data regarding animal feed concentrates. Optional indexing with the index parameter.

        Args:
            index (str): The column to use as the DataFrame index.

        Returns:
            pd.DataFrame: A DataFrame containing concentrate feed data.
        """
        table = "concentrate_database"

        if index == None:
            dataframe = pd.read_sql("SELECT * FROM '%s'" % (table), self.engine)

        else:
            dataframe = pd.read_sql(
                "SELECT * FROM '%s'" % (table),
                self.engine,
                index_col=[index],
            )

        return dataframe


    def animal_features_data(self, index=None):
        """
        Collects data related to the features of various animal types, filtered by country. Indexing option available.

        Args:
            index (str): The column to use as the DataFrame index.

        Returns:
            pd.DataFrame: A DataFrame containing animal features data.
        """
        table = "animal_features_database"

        if index == None:
            dataframe = pd.read_sql(
                "SELECT * FROM '%s' WHERE ef_country = '%s'" % (table, self.ef_country),
                self.engine,
            )

        else:
            dataframe = pd.read_sql(
                "SELECT * FROM '%s' WHERE ef_country = '%s'" % (table, self.ef_country),
                self.engine,
                index_col=[index],
            )

        return dataframe
