#!/usr/bin/python

# this is the main script for the hyaloclastite

import argparse
import curses

from time import sleep

from functions.vieweractions import is_viewer_regular_action

parser = argparse.ArgumentParser(prog = "hyalo.py",
                                 description = "Python curses program for terminal note-taking.")

### parse and verify arguments
parser.add_argument(dest="vault", type=str, help="Directory with your project.")
arguments = parser.parse_args()

vault_name = arguments.vault

def main(stdscr, vault):

    ### program constants
    # this might be read from a config file in the future, or be set depending on start options
    start_mode = 'filebrowser'
    old_mode = start_mode
    mode_changed = False

    stdscr.clear()
    mode = start_mode

    while True:
        if mode_changed:
            hyaloclastite_initialise(stdscr, mode, vault)
            mode_changed = False
        sleep(0.1)
        control_char = stdscr.getkey()
        if is_action_quit(control_char):
            exit_program(0)
        elif mode == 'viewer':
            if is_viewer_regular_action(control_char):
                perform_viewer_action(stdscr, vault, control_char)
            elif is_viewer_switch_mode(control_char):
                old_mode = mode
                mode = switch_mode(stdscr, vault, control_char)
                mode_changed = True
        elif mode == 'filebrowser':
            if is_filebrowser_regular_action(control_char):
                perform_filebrowser_action(stdscr, vault, control_char)
            elif is_filebrowser_switch_mode(control_char):
                old_mode = mode
                switch_mode(stdscr, vault, control_char)
                mode_changed = True

# start the program in the default mode
curses.wrapper(main, vault_name)
