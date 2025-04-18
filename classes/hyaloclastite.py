#!/usr/bin/python
import curses 
from time import sleep

class hyaloclastite:
    def __init__(self, initial_mode, vault):
        self.window = None
        self.mode = initial_mode
        self.vault = vault
        self.exitcharacter = ord('q')

    def check_for_exit(self, control_char):
        if control_char == self.exitcharacter:
            return True
        else:
            return False

    def perform_action(self, control_char):
        pass

    def draw(self):
        pass

    def main(self, stdscr, vault, mode):
        self.window = stdscr
        while True:
            self.draw()
            sleep(0.1)
            control_char = stdscr.getch()
            if self.check_for_exit(control_char):
                return 0
            self.perform_action(control_char)
        return 1 # this should not happen

    def run(self):
        """Start the program with vault_name and initial_mode arguments.
        Use curses wrapper to take care of terminal state cleanup."""
        return curses.wrapper(self.main, self.vault, self.mode)

