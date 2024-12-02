import unittest
from workbench.dataloader import DataLoader
from workbench.countryinfo import CountryInfo
from workbench.city import City

class TestDataLoader(unittest.TestCase):

    def setUp(self):
        self.data_loader = DataLoader()

    def test_loadCityPatches(self):
        city_patches = self.data_loader.loadCityPatches()
        self.assertIsInstance(city_patches, dict)
        # Add assertions for expected content if known

    def test_loadCountryInfo(self):
        country_info = self.data_loader.loadCountryInfo()
        self.assertIsInstance(country_info, dict)
        # Check for specific country
        if "US" in country_info:
            self.assertIsInstance(country_info["US"], CountryInfo)

    def test_loadNationalities(self):
        nationalities = self.data_loader.loadNationalities()
        self.assertIsInstance(nationalities, dict)
        # Check for specific nationality
        self.assertIn("afghan", nationalities)

    def test_loadCities(self):
        cities = self.data_loader.loadCities()
        self.assertIsInstance(cities, list)
        if cities:
            self.assertIsInstance(cities[0], City)

if __name__ == '__main__':
    unittest.main()