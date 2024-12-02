import unittest
from workbench.lice.models.license_file import LicenseFile

class TestLicenseFile(unittest.TestCase):
    def setUp(self):
        self.license_file = LicenseFile('mit', 2022, 'ExampleOrg', 'Sample Content')

    def test_license_file_initialization(self):
        self.assertEqual(self.license_file.type, 'mit')
        self.assertEqual(self.license_file.year, 2022)
        self.assertEqual(self.license_file.organization, 'ExampleOrg')
        self.assertEqual(self.license_file.content, 'Sample Content')

    def test_save_to_file(self):
        self.license_file.saveToFile('test_license.txt')
        with open('test_license.txt', 'r') as f:
            content = f.read()
        self.assertEqual(content, 'Sample Content')

if __name__ == "__main__":
    unittest.main()