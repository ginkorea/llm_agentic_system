import unittest
from workbench.dataloader import DataLoader

class TestDataLoader(unittest.TestCase):

    def setUp(self):
        self.data_loader = DataLoader()

    def test_loadCityPatches(self):
        city_patches = self.data_loader.loadCityPatches()
        self.assertIsInstance(city_patches, dict)

    def test_loadCountryInfo(self):
        country_info = self.data_loader.loadCountryInfo()
        self.assertIsInstance(country_info, dict)

    def test_loadNationalities(self):
        nationalities = self.data_loader.loadNationalities()
        self.assertIsInstance(nationalities, dict)

    def test_loadCities(self):
        cities = self.data_loader.loadCities()
        self.assertIsInstance(cities, list)

if __name__ == '__main__':
    unittest.main()