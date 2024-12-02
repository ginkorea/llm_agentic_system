import unittest
from results.hone.hone.JSONGenerator import JSONGenerator

class TestJSONGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = JSONGenerator()
        self.sample_data = [
            ["Alice", "30", "New York"],
            ["Bob", "25", "Los Angeles"]
        ]
        self.sample_schema = {"name": "name", "age": "age", "city": "city"}

    def test_convertToJSON(self):
        expected_json = '[\n  {\n    "age": "30",\n    "city": "New York",\n    "name": "Alice"\n  },\n  {\n    "age": "25",\n    "city": "Los Angeles",\n    "name": "Bob"\n  }\n]'
        json_data = self.generator.convertToJSON(self.sample_data, self.sample_schema)
        self.assertEqual(json_data, expected_json)

    def test_generateSchema(self):
        column_names = ["name", "age", "city"]
        expected_schema = {"name": "name", "age": "age", "city": "city"}
        schema = self.generator.generateSchema(column_names)
        self.assertEqual(schema, expected_schema)

if __name__ == '__main__':
    unittest.main()