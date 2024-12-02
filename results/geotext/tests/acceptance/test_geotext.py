import unittest
from workbench.geotext import GeoText
from workbench.location import Location

class TestGeoText(unittest.TestCase):

    def setUp(self):
        self.geo_text = GeoText()

    def test_extractCitiesAndCountries(self):
        text = "New York is a city in the United States."
        locations = self.geo_text.extractCitiesAndCountries(text)
        self.assertIsInstance(locations, list)
        self.assertTrue(any(loc.name == "New York" and loc.type == "city" for loc in locations))

    def test_filterByCountryCode(self):
        locations = [Location("New York", "city", "US"), Location("Toronto", "city", "CA")]
        filtered_locations = self.geo_text.filterByCountryCode(locations, "US")
        self.assertEqual(len(filtered_locations), 1)
        self.assertEqual(filtered_locations[0].name, "New York")

    def test_countCountryMentions(self):
        text = "The United States and Canada are neighboring countries."
        country_count = self.geo_text.countCountryMentions(text)
        self.assertIsInstance(country_count, dict)
        self.assertEqual(country_count.get("US"), 1)
        self.assertEqual(country_count.get("CA"), 1)

if __name__ == '__main__':
    unittest.main()