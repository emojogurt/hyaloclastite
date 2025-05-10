#!/usr/bin/python
import argparse

parser = argparse.ArgumentParser(prog = "parrot.py", description = "This program saves arguments used to call it under parrotargs.txt.")

parser.add_argument(dest="all_params", nargs='+')
arguments = parser.parse_args()

with open("parrotargs.txt", 'w') as parrotfile:
    parrotfile.write(str(arguments.all_params))