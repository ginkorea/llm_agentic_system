import unittest
from workbench.lice.models.command import Command

class TestCommand(unittest.TestCase):
    def test_command_initialization(self):
        parameters = {'license': 'mit', 'year': 2022, 'org': 'ExampleOrg'}
        command = Command(type='mit', parameters=parameters)
        self.assertEqual(command.type, 'mit')
        self.assertEqual(command.parameters, parameters)

if __name__ == "__main__":
    unittest.main()