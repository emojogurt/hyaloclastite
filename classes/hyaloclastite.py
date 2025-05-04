#!/usr/bin/python
import curses 

from os import scandir
from os.path import basename, join

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

        if self.current_selected_file not in keylist:
            self.current_selected_file = keylist[0]
            self.current_selected_file_number = 0

        self.current_directory_listing = {}
        for fsobjname in keylist:
            self.current_directory_listing[fsobjname] = listing_dict_unsorted[fsobjname]

    def draw(self, window):
        window.clear()
        if self.mode == 'filebrowser':
            # new_rows = len(self.current_directory_listing) + 2
            # new_cols = max([len(x) for x in list(self.current_directory_listing.keys())])
            # window.resize(new_rows, new_cols)
            window.addstr(basename(self.current_directory))
            for listing_key,fsobject_entry in self.current_directory_listing.items():
                parameters = 0
                if fsobject_entry.is_dir():
                    parameters = parameters | curses.A_BOLD
                if fsobject_entry.name == self.current_selected_file:
                    parameters = parameters | curses.A_REVERSE
                window.addstr("\n " + listing_key, parameters)
        elif self.mode == 'viewer':
            with open(join(self.current_directory, self.current_selected_file), 'r') as viewed_file:
                content = viewed_file.readlines()
                new_lines = len(content) + 1
                new_cols = max([len(x) for x in content])
                title = basename(self.current_selected_file)
                new_cols = max(new_cols, len(title)) + 1
                window.resize(new_lines, new_cols)
                window.addstr(title)
                window.addstr('\n')
                for line in content:
                    window.addstr(line)
        window.refresh(0, 0, 0, 0, curses.LINES - 1, curses.COLS - 1)

    def perform_filebrowser_action(self, window, control_char):
        if control_char == curses.KEY_DOWN and self.current_selected_file_number < len(self.current_directory_listing) - 1:
            self.current_selected_file_number += 1
            self.current_selected_file = list(self.current_directory_listing.keys())[self.current_selected_file_number]
        elif control_char == curses.KEY_UP and self.current_selected_file_number > 0:
            self.current_selected_file_number -= 1
            self.current_selected_file = list(self.current_directory_listing.keys())[self.current_selected_file_number]
        elif control_char == ord('v'):
            self.mode = 'viewer'

    def perform_viewer_action(self, window, control_char):
        if control_char == ord('c'):
            self.mode = 'filebrowser'

    def dispatch_action(self, window, control_char):
        """Sends the control character towards the appropriate handling function, depending on mode"""
        if self.mode == 'filebrowser':
            self.perform_filebrowser_action(window, control_char)
        elif self.mode == 'viewer':
            self.perform_viewer_action(window, control_char)
        else:
            raise IncorrectModeException
    
    def check_for_exit(self, control_char):
        if control_char == self.exit_character:
            return True
        else:
            return False

    def start(self):
        # TODO remove this function and instead add a bool 'refresh_needed' that will be checked in 'draw' and set
        # TODO (cont.) in every other place where a refresh might be needed
        if self.mode == 'filebrowser':
            self.get_dir_contents()

    def main(self, window, vault, mode):
        """Main loop of the program, taking care of gathering user input and providing it to appropriate functions"""
        self.start()
        while True:
            self.draw(window)
            control_char = window.getch()
            if self.check_for_exit(control_char):
                return 0
            self.dispatch_action(window, control_char)

    def run(self):
        """Starts the program with vault_name and initial_mode arguments.
        Takes care of terminal state cleanup."""
        curses.initscr()
        window = curses.newpad(20,20) # this should be initialised to be small and resized when new file or directory is opened
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
        self.current_directory_listing = None
        self.current_selected_file = None
        self.current_selected_file_number = None
