#!/usr/bin/python

# this is the main script for the hyaloclastite

import argparse
import curses

from time import sleep
from classes.hyaloclastite import hyaloclastite

parser = argparse.ArgumentParser(prog = "hyalo.py",
                                 description = "Python curses program for terminal note-taking.")

### parse and verify arguments
parser.add_argument(dest="vault", type=str, help="Directory with your project.")
arguments = parser.parse_args()

vault_name = arguments.vault

# this might be read from a config file in the future, or be set depending on start options
initial_mode = 'filebrowser'

def main(stdscr, vault, mode):
    
    session = hyaloclastite(stdscr, mode, vault)

    while True:
        sleep(0.1)
        control_char = stdscr.getkey()
        session.perform_action(control_char)

# start the program in the initial mode
curses.wrapper(main, vault_name, initial_mode)
