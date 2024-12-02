import unittest
from workbench.city import City

class TestCity(unittest.TestCase):

    def test_city_initialization(self):
        city = City(1, "New York", 40.7128, -74.0060, "US")
        self.assertEqual(city.id, 1)
        self.assertEqual(city.name, "New York")
        self.assertEqual(city.latitude, 40.7128)
        self.assertEqual(city.longitude, -74.0060)
        self.assertEqual(city.countryCode, "US")

if __name__ == '__main__':
    unittest.main()