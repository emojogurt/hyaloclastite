#!/usr/bin/python
import curses 
from time import sleep

class IncorrectModeException(Exception):
    pass

class Hyaloclastite:
    def __init__(self, initial_mode, vault):
        self.mode = initial_mode
        self.vault = vault
        self.exit_character = ord('q')

    def check_for_exit(self, control_char):
        if control_char == self.exit_character:
            return True
        else:
            return False

    def perform_filebrowser_action(self, window, control_char):
        pass

    def perform_viewer_action(self, window, control_char):
        pass

    def dispatch_action(self, window, control_char):
        if self.mode == 'filebrowser':
            self.perform_filebrowser_action(window, control_char)
        elif self.mode == 'viewer':
            self.perform_viewer_action(window, control_char)
        else:
            raise IncorrectModeException

    def draw(self, window):
        pass

    def main(self, window, vault, mode):
        """Main loop of the program, taking care of gathering user input and providing it to appropriate functions"""

        while True:
            self.draw(window)
            sleep(0.1)
            control_char = window.getch()
            if self.check_for_exit(control_char):
                return 0
            self.dispatch_action(window, control_char)

    def run(self):
        """Starts the program with vault_name and initial_mode arguments.
        Takes care of terminal state cleanup."""
        window = curses.initscr()
        curses.noecho()
        curses.curs_set(False)
        curses.cbreak()
        window.keypad(True)

        try:
            self.main(window, self.vault, self.mode)
        except Exception as e:
            raise e
        finally:
            curses.nocbreak()
            window.keypad(False)
            curses.echo()
            curses.endwin()

