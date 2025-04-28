#!/usr/bin/python
import curses 
from time import sleep
from os import scandir
from os.path import basename

class IncorrectModeException(Exception):
    pass

class Hyaloclastite:
    def get_dir_contents(self):
        raw_listing = scandir(self.current_directory)
        listing_dict_unsorted = {}
        for fsobject in raw_listing:
            listing_dict_unsorted[fsobject.name] = fsobject

        keylist = list(listing_dict_unsorted.keys())
        keylist.sort()
        
        listing_dict = {}
        for fsobjname in keylist:
            listing_dict[fsobjname] = listing_dict_unsorted[fsobjname]
        return listing_dict

    def create_screen_contents(self):
        if self.mode == 'filebrowser':
            screen_contents = basename(self.current_directory)
            listing_dict = self.get_dir_contents()
            for listing_key,fsobject_entry in listing_dict.items():
                if fsobject_entry.is_dir():
                    screen_contents += "\n > " + listing_key
                else:
                    screen_contents += "\n " + listing_key
            return screen_contents
        else:
            return "Nothing to see here"

    def check_for_exit(self, control_char):
        if control_char == self.exit_character:
            return True
        else:
            return False

    def draw(self, window):
        """Displays previously prepared window contents to the given window"""
        window.clear()
        window.addstr(self.current_screen_contents)
        window.refresh()

    def perform_filebrowser_action(self, window, control_char):
        pass

    def perform_viewer_action(self, window, control_char):
        pass

    def dispatch_action(self, window, control_char):
        """Sends the control character towards the appropriate handling function, depending on mode"""
        if self.mode == 'filebrowser':
            self.perform_filebrowser_action(window, control_char)
        elif self.mode == 'viewer':
            self.perform_viewer_action(window, control_char)
        else:
            raise IncorrectModeException

    def main(self, window, vault, mode):
        """Main loop of the program, taking care of gathering user input and providing it to appropriate functions"""

        while True:
            self.draw(window)
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
        window.nodelay(False)

        try:
            self.main(window, self.vault, self.mode)
        except Exception as e:
            raise e
        finally:
            curses.nocbreak()
            window.keypad(False)
            curses.echo()
            curses.endwin()

    def __init__(self, initial_mode, vault):
        self.mode = initial_mode
        self.vault = vault
        self.exit_character = ord('q')
        self.current_directory = self.vault
        self.current_screen_contents = self.create_screen_contents()
        self.current_directory_listing = None
        self.current_selected_file = None

