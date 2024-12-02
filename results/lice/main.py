from workbench.lice.cli import CLI

if __name__ == "__main__":
    cli = CLI()
    command = cli.parseArguments(['bsd3', '--year', '2021', '--org', 'ExampleOrg'])
    cli.executeCommand(command)