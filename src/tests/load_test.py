import unittest
import pandas as pd
import os

from cattle_lca.models import Animal_Features, Grass, Concentrate, Upstream, Emissions_Factors

    
class DatasetLoadingTestCase(unittest.TestCase):
        
    def setUp(self):
        self.data_dir = "./data"

    def test_dataset_loading(self):
        # Test loading the datasets as pandas DataFrames
        animal_features_path = os.path.join(self.data_dir, "animal_features_database.csv")
        concentrate_path = os.path.join(self.data_dir, "concentrate_database.csv")
        ef_path = os.path.join(self.data_dir, "emissions_factors_database.csv")
        grass_path = os.path.join(self.data_dir, "grass_database.csv")
        upstream_path = os.path.join(self.data_dir, "upstream_database.csv")
       

        # Load the datasets as DataFrames
        animal_features = pd.read_csv(animal_features_path, index_col = 0)
        concentrate = pd.read_csv(concentrate_path, index_col = 0)
        ef = pd.read_csv(ef_path, index_col = 0)
        grass = pd.read_csv(grass_path, index_col = 0)
        upstream = pd.read_csv(upstream_path, index_col = 0)

        # Perform assertions to validate the loaded data

        animal_class = Animal_Features(animal_features)
        concentrate_class = Concentrate(concentrate)
        ef_class = Emissions_Factors(ef)
        grass_class = Grass(grass)
        upstream_class = Upstream(upstream)

        self.assertTrue(animal_class.is_loaded())
        self.assertTrue(concentrate_class.is_loaded())
        self.assertTrue(ef_class.is_loaded())
        self.assertTrue(grass_class.is_loaded())
        self.assertTrue(upstream_class.is_loaded())


if __name__ == "__main__":
    unittest.main()
