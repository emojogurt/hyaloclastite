#!/usr/bin/python

"""
This is the main definition of hyaloclastite.
To use it, you will need to create an istance of hyaloclastite class and call its run method.
Arguments that must be supplied are mode (for now only 'filebrowser' is supported), and
vault (top-level directory where your content resides).
"""

import curses
import subprocess

from os import scandir, environ
from os.path import abspath, basename, join, samefile, normpath
import pathlib

class IncorrectModeException(Exception):
    """Thrown when the mode is not one of the recognised ones, 'filebrowser' or 'viewer'"""


class Hyaloclastite:
    """
    Main class. Create instance of it, supplying mode and vault.
    Mode can for now only be 'filebrowser'.
    Vault is the top-level directory where your content resides.
    """
    def get_dir_contents(self):
        """
        :return: nothing
        this function lists contents of the directory where the program currently is,
        taking care to add a link to parent dir unless the program is already at the vault top level
        """
        raw_listing = scandir(self.current_directory)
        listing_dict_unsorted = {}
        for fsobject in raw_listing:
            listing_dict_unsorted[fsobject.name] = fsobject

        keylist = list(listing_dict_unsorted.keys())
        keylist.sort()

        if samefile(self.current_directory, self.vault):
            self.current_directory_listing = []
        else:
            self.current_directory_listing = [pathlib.Path(join(self.current_directory, '..'))]
        for fsobjname in keylist:
            self.current_directory_listing.append(listing_dict_unsorted[fsobjname])

        self.current_selected_file_number = 0

    def draw(self, window):
        """
        :param window: curses pad, where the content is supposed to be drawn
        :return: nothing
        this function draws contents appropriate for the current mode in the given window
        """
        window.clear()
        if self.mode == 'filebrowser':
            if self.dir_read_needed:
                self.get_dir_contents()
                self.dir_read_needed = False
            new_lines = max(len(self.current_directory_listing), curses.LINES) + 2
            new_cols = max(len(x.name) for x in self.current_directory_listing)
            if samefile(self.current_directory, self.vault):
                title = basename(self.vault)
            else:
                title = basename(self.vault) + "/" + basename(self.current_directory)
            new_cols = max([new_cols, len(title), curses.COLS]) + 1
            window.resize(new_lines, new_cols)
            window.addstr(title)
            for fs_entry_number, fsobject_entry in enumerate(self.current_directory_listing):
                parameters = 0
                if fsobject_entry.is_dir():
                    parameters = parameters | curses.A_BOLD
                if fs_entry_number == self.current_selected_file_number:
                    parameters = parameters | curses.A_REVERSE
                window.addstr("\n " + fsobject_entry.name, parameters)
            window.refresh(self.current_browser_view_offset, 0, 0, 0, curses.LINES - 1, curses.COLS - 1)
        elif self.mode == 'viewer':
            filepath = self.current_directory_listing[self.current_selected_file_number].name
            filepath = join(self.current_directory, filepath)
            with open(filepath, 'r', encoding=self.file_encoding) as viewed_file:
                content = viewed_file.readlines()
                if len(content) == 0:
                    content = ['<file is empty>']
                new_lines = max(len(content), curses.LINES) + 2
                new_cols = max(len(x) for x in content)
                title = basename(self.current_directory_listing[self.current_selected_file_number].name)
                new_cols = max([new_cols, len(title), curses.COLS]) + 1
                window.resize(new_lines, new_cols)
                window.addstr(title)
                window.addstr('\n')
                for line in content:
                    window.addstr(line)
            window.refresh(self.current_position_in_file, 0, 0, 0, curses.LINES - 1, curses.COLS - 1)


    def launch_editor(self):
        """
        :return: nothing
        this function runs whatever command saved under EDITOR environment variable
        """
        editor = environ['EDITOR']
        filepath = self.current_directory_listing[self.current_selected_file_number].name
        filepath = join(self.current_directory, filepath)
        subprocess.run([editor, filepath], check=False)

    def perform_filebrowser_action(self, window, control_char):
        """
        :param window: window where the contents of the program are drawn,
        only passed here to make sure it is returned to a proper state after the editor finishes
        :param control_char: an integer representing a key, resulting from getch() as per
        curses specification
        :return: nothing
        """
        if control_char == curses.KEY_DOWN and self.current_selected_file_number < len(self.current_directory_listing) - 1:
            self.current_selected_file_number += 1
        elif control_char == curses.KEY_UP and self.current_selected_file_number > 0:
            self.current_selected_file_number -= 1
        elif control_char == ord('v'):
            if not self.current_directory_listing[self.current_selected_file_number].is_dir():
                self.mode = 'viewer'
                self.current_position_in_file = 0
            else:
                subdirpath = self.current_directory_listing[self.current_selected_file_number].name
                subdirpath = join(self.current_directory, subdirpath)
                self.current_directory = normpath(subdirpath)
                self.dir_read_needed = True
        elif control_char == ord('e'):
            curses.def_prog_mode()
            self.launch_editor()
            curses.reset_prog_mode()
            window.leaveok(True)
        # adjust file browser view position:
        while self.current_selected_file_number > self.current_browser_view_offset + curses.LINES - 2:
            self.current_browser_view_offset += curses.LINES
        while self.current_selected_file_number < self.current_browser_view_offset - 1:
            self.current_browser_view_offset -= curses.LINES

    def perform_viewer_action(self, window, control_char):
        """
        :param window: window where the contents of the program are drawn,
        only passed here to make sure it is returned to a proper state after the editor finishes
        :param control_char: an integer representing a key, resulting from getch() as per
        curses specification
        :return: nothing
        """
        if control_char == ord('c'):
            self.mode = 'filebrowser'
        elif control_char == curses.KEY_DOWN and self.current_position_in_file < window.getmaxyx()[0] + 1 - curses.LINES:
            self.current_position_in_file += 1
        elif control_char == curses.KEY_UP and self.current_position_in_file > 0:
            self.current_position_in_file -= 1
        elif control_char == ord('e'):
            curses.def_prog_mode()
            self.launch_editor()
            curses.reset_prog_mode()
            window.leaveok(True)

    def dispatch_action(self, window, control_char):
        """
        :param window: window where the contents of the program are drawn,
        only passed here to make sure it is returned to a proper state after the editor finishes
        :param control_char: an integer representing a key, resulting from getch() as per
        curses specification
        Sends the control character towards the appropriate handling function, depending on mode"""
        if self.mode == 'filebrowser':
            self.perform_filebrowser_action(window, control_char)
        elif self.mode == 'viewer':
            self.perform_viewer_action(window, control_char)
        else:
            raise IncorrectModeException

    def check_for_exit(self, control_char):
        """
        :param control_char: an integer representing a key, resulting from getch() as per
        curses specification
        :return: True if the control_char is the key used to close the program, False otherwise
        """
        return bool(control_char == self.exit_character)

    def main(self, window):
        """Main loop of the program, gathers user input and provides it to appropriate functions"""
        self.dir_read_needed = True
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
        window = curses.newpad(20,20) # resized when new file or directory is opened
        curses.noecho()
        curses.curs_set(False)
        curses.cbreak()
        curses.curs_set(0)
        window.keypad(True)
        window.nodelay(False)
        window.leaveok(True)

        try:
            self.main(window)
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
        self.file_encoding = 'utf-8'
        self.dir_read_needed = None
        self.current_directory = abspath(self.vault)
        self.current_directory_listing = None
        self.current_selected_file_number = None
        self.current_browser_view_offset = 0
        self.current_position_in_file = None
