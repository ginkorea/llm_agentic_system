import unittest
from workbench.lice.template_manager import TemplateManager

class TestTemplateManager(unittest.TestCase):
    def setUp(self):
        self.manager = TemplateManager()

    def test_get_template(self):
        template = self.manager.getTemplate('mit')
        self.assertEqual(template, "Template Content")

    def test_add_template(self):
        result = self.manager.addTemplate('new_template_path')
        self.assertTrue(result)

    def test_list_templates(self):
        templates = self.manager.listTemplates()
        self.assertIn("template1", templates)
        self.assertIn("template2", templates)

if __name__ == "__main__":
    unittest.main()