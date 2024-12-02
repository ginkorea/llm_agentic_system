import unittest
from workbench.location import Location

class TestLocation(unittest.TestCase):

    def test_location_initialization(self):
        loc = Location("New York", "city", "US")
        self.assertEqual(loc.name, "New York")
        self.assertEqual(loc.type, "city")
        self.assertEqual(loc.countryCode, "US")

if __name__ == '__main__':
    unittest.main()