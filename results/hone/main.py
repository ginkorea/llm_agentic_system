# main.py
from results.hone.hone.CLI import CLI

if __name__ == "__main__":
    cli = CLI()
    args = cli.parseArguments()
    cli.executeConversion(args)