import argparse
from .license_generator import LicenseGenerator
from .models.command import Command

class CLI:
    def parseArguments(self, args):
        parser = argparse.ArgumentParser(description="License Generator CLI")
        parser.add_argument('license', type=str, help='Type of license to generate')
        parser.add_argument('-y', '--year', type=int, help='Year for the license')
        parser.add_argument('-o', '--org', type=str, help='Organization for the license')
        parsed_args = parser.parse_args(args)
        return Command(type=parsed_args.license, parameters=vars(parsed_args))

    def executeCommand(self, command):
        generator = LicenseGenerator()
        license_file = generator.generateLicense(command.parameters['license'], command.parameters['year'], command.parameters['org'])
        license_file.saveToFile("LICENSE")