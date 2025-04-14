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
            action = process_viewer_input(control_char)
            if is_viewer_action_correct(action):
                perform_viewer_action(action)
            elif is_action_quit(action):
                exit_program(0)
            elif is_action_switchmode(action):
                switch_mode(action)
        elif mode == 'filebrowser':
            action = process_filebrowser_input(control_char)
            if is_filebrowser_action_correct(action):
                perform_filebrowser_action(action)
            elif is_action_quit(action):
                exit_program(0)
            elif is_action_switchmode(action):
                switch_mode(action)
        # this is probably useless, editor should not be a mode
        elif mode == 'editor':
            sleep(0.2)
            pass
        sleep(0.05)

# start the program in the default mode
curses.wrapper(main)
