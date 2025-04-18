#!/usr/bin/python
import curses 
from time import sleep

class Hyaloclastite:
    def __init__(self, initial_mode, vault):
        self.window = None
        self.mode = initial_mode
        self.vault = vault
        self.exit_character = ord('q')

    def check_for_exit(self, control_char):
        if control_char == self.exit_character:
            return True
        else:
            return False

    def perform_action(self, control_char):
        pass

    def draw(self):
        pass

    def main(self, window, vault, mode):
        """Main loop of the program, taking care of gathering user input and providing it to appropriate functions"""

        while True:
            self.draw()
            sleep(0.1)
            control_char = window.getch()
            if self.check_for_exit(control_char):
                return 0
            self.perform_action(control_char)

    def run(self):
        """Starts the program with vault_name and initial_mode arguments.
        Takes care of terminal state cleanup."""
        self.window = curses.initscr()
        curses.noecho()
        curses.curs_set(False)
        curses.cbreak()
        self.window.keypad(True)

        try:
            self.main(self.window, self.vault, self.mode)
        except Exception as e:
            raise e
        finally:
            curses.nocbreak()
            self.window.keypad(False)
            curses.echo()
            curses.endwin()

        #return curses.wrapper(self.main, self.vault, self.mode)

