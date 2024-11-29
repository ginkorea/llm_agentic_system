# example_script.py
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--arg1", type=str, help="An example argument")
parser.add_argument("--flag", action="store_true", help="An example flag")
args = parser.parse_args()

print(f"arg1: {args.arg1}")
print(f"flag: {args.flag}")
