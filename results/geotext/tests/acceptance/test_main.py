import unittest
from workbench.geotext import GeoText
from workbench.location import Location

class TestMainFlow(unittest.TestCase):

    def setUp(self):
        self.geo_text = GeoText()

    def test_main_flow(self):
        text = "Paris is a beautiful city in France."
        locations = self.geo_text.extractCitiesAndCountries(text)
        self.assertIsInstance(locations, list)
        self.assertTrue(any(loc.name == "Paris" and loc.type == "city" for loc in locations))

        filtered_locations = self.geo_text.filterByCountryCode(locations, "FR")
        self.assertEqual(len(filtered_locations), 1)
        self.assertEqual(filtered_locations[0].name, "Paris")

        country_count = self.geo_text.countCountryMentions(text)
        self.assertIsInstance(country_count, dict)
        self.assertEqual(country_count.get("FR"), 1)

if __name__ == '__main__':
    unittest.main()