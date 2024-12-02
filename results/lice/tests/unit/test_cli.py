import unittest
from workbench.lice.cli import CLI
from workbench.lice.models.command import Command

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.cli = CLI()

    def test_parse_arguments(self):
        args = ['mit', '--year', '2022', '--org', 'ExampleOrg']
        command = self.cli.parseArguments(args)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.type, 'mit')
        self.assertEqual(command.parameters['year'], 2022)
        self.assertEqual(command.parameters['org'], 'ExampleOrg')

    def test_parse_arguments_missing_optional(self):
        args = ['gpl3']
        command = self.cli.parseArguments(args)
        self.assertEqual(command.type, 'gpl3')
        self.assertIsNone(command.parameters.get('year'))
        self.assertIsNone(command.parameters.get('org'))

    def test_execute_command(self):
        command = Command(type='bsd3', parameters={'license': 'bsd3', 'year': 2023, 'org': 'ExampleOrg'})
        self.cli.executeCommand(command)
        with open("LICENSE", 'r') as f:
            content = f.read()
        self.assertIn("Template Content for ExampleOrg in 2023 using Python", content)

if __name__ == "__main__":
    unittest.main()