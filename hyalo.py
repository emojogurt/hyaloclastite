#!/usr/bin/python

# this is the main script for the hyaloclastite

import argparse
import curses

from time import sleep

parser = argparse.ArgumentParser(prog = "hyalo.py",
                                 description = "Python curses program for terminal note-taking.")

### parse and verify arguments
parser.add_argument(dest="vault", type=str, help="Directory with your project.")
arguments = parser.parse_args()

vault = arguments.vault

### program constants
# this might be read from a config file in the future, or depending on start options
start_mode = 'filebrowser'

# define the main program loop
def main(stdscr):
    stdscr.clear()
    mode = start_mode
    while(True):
        control_char = stdscr.getkey()
        if mode == 'viewer':
            if is_viewer_action_correct(control_char):
                perform_viewer_action(control_char)
            elif is_action_quit(control_char):
                exit_program(0)
            elif is_action_switchmode(control_char):
                switch_mode(control_char)
        elif mode == 'filebrowser':
            if is_filebrowser_action_correct(control_char):
                perform_filebrowser_action(control_char)
            elif is_action_quit(control_char):
                exit_program(0)
            elif is_action_switchmode(control_char):
                switch_mode(control_char)

# start the program in the default mode
curses.wrapper(main)
