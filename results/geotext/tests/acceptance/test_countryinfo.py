import unittest
from workbench.countryinfo import CountryInfo

class TestCountryInfo(unittest.TestCase):

    def test_countryinfo_initialization(self):
        country_info = CountryInfo("US", "United States", "Washington, D.C.", 9833517, 331002651, ["en"])
        self.assertEqual(country_info.iso, "US")
        self.assertEqual(country_info.name, "United States")
        self.assertEqual(country_info.capital, "Washington, D.C.")
        self.assertEqual(country_info.area, 9833517)
        self.assertEqual(country_info.population, 331002651)
        self.assertEqual(country_info.languages, ["en"])

if __name__ == '__main__':
    unittest.main()