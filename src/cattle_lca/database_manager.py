import sqlalchemy as sqa
import pandas as pd
from cattle_lca.database import get_local_dir
import os


class DataManager:
    def __init__(self, ef_country):
        self.database_dir = get_local_dir()
        self.engine = self.data_engine_creater()
        self.ef_country = ef_country

    def data_engine_creater(self):
        database_path = os.path.abspath(
            os.path.join(self.database_dir, "cattle_database.db")
        )
        engine_url = f"sqlite:///{database_path}"

        return sqa.create_engine(engine_url)

    def grass_data(self, index=None):
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
