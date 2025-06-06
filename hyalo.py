#!/usr/bin/python

# this is the main script for the hyaloclastite
# mostly a wrapper to pass arguments to the hyaloclastite.run() function

import argparse
from os import path

from classes.hyaloclastite import Hyaloclastite

parser = argparse.ArgumentParser(prog = "hyalo.py",
                                 description = "Python curses program for terminal note-taking.")

### parse and verify arguments
parser.add_argument(dest="vault", type=str, help="Directory with your project.")
arguments = parser.parse_args()

vault_name = path.abspath(arguments.vault)

# this might be read from a config file in the future, or be set depending on start options
initial_mode = 'filebrowser'

session = Hyaloclastite(initial_mode, vault_name)
rc = session.run()
exit(rc)
