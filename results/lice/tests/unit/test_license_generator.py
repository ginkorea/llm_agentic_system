import unittest
from workbench.lice.license_generator import LicenseGenerator
from workbench.lice.models.license_file import LicenseFile

class TestLicenseGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = LicenseGenerator()

    def test_generate_license(self):
        license_file = self.generator.generateLicense('gpl3', 2021, 'ExampleOrg')
        self.assertIsInstance(license_file, LicenseFile)
        self.assertEqual(license_file.type, 'gpl3')
        self.assertEqual(license_file.year, 2021)
        self.assertEqual(license_file.organization, 'ExampleOrg')

    def test_list_available_licenses(self):
        templates = self.generator.listAvailableLicenses()
        self.assertIn("template1", templates)
        self.assertIn("template2", templates)

    def test_add_custom_template(self):
        result = self.generator.addCustomTemplate('path/to/custom/template')
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()