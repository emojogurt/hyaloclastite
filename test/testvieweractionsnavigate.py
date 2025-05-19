#!/usr/bin/python

import unittest
import sys
from os import path, removedirs, remove, mkdir, listdir

import fakeCurses
import curses

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from classes.hyaloclastite import Hyaloclastite

class TestViewerActions(unittest.TestCase):
    def setUp(self):
        curses.initscr()
        self.file_name = 'a_file'
        self.directory_name = "testvault_generated"
        self.base_directory = path.dirname(path.dirname(path.abspath(__file__)))
        self.test_location = path.join(self.base_directory, self.directory_name)
        mkdir(self.test_location)
        with open(path.join(self.test_location, self.file_name), 'w') as file1:
            file1.write('line 1')

        with open(path.join(self.test_location, self.file_name), 'a') as genfile:
            test = curses.LINES + 51
            for line_num in range(2, curses.LINES + 51):
                genfile.write('\nline ' + str(line_num))

    def tearDown(self):
        for filename in listdir(self.test_location):
            remove(path.join(self.test_location, filename))
        removedirs(self.test_location)

        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def test_initial_position_zero(self):
        sess = Hyaloclastite('filebrowser', self.test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        sess.current_selected_file = self.file_name
        sess.current_selected_file_number = 1
        sess.dispatch_action(window, ord('v'))
        self.assertEqual(sess.current_position_in_file, 0)

    def test_downarrow_scrolls_down(self):
        sess = Hyaloclastite('filebrowser', self.test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        sess.current_selected_file = self.file_name
        sess.current_selected_file_number = 1
        sess.dispatch_action(window, ord('v'))
        sess.draw(window)
        sess.perform_viewer_action(window, curses.KEY_DOWN)
        self.assertEqual(sess.current_position_in_file, 1)

    def test_uparrow_scrolls_up(self):
        sess = Hyaloclastite('filebrowser', self.test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        sess.current_selected_file = self.file_name
        sess.current_selected_file_number = 1
        sess.dispatch_action(window, ord('v'))
        sess.draw(window)
        sess.current_position_in_file = 3
        sess.perform_viewer_action(window, curses.KEY_UP)
        self.assertEqual(sess.current_position_in_file, 2)

    def test_no_scroll_down_when_bottom_reached(self):
        sess = Hyaloclastite('filebrowser', self.test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        sess.current_selected_file = self.file_name
        sess.current_selected_file_number = 1
        sess.dispatch_action(window, ord('v'))
        sess.draw(window)
        for i in range(60):
            sess.perform_viewer_action(window, curses.KEY_DOWN)
        self.assertEqual(53, sess.current_position_in_file) # max position is: 1 (title) + file length (lines + 50) + 2 (added when resizing) - lines.

    def test_no_scroll_up_when_top_reached(self):
        sess = Hyaloclastite('filebrowser', self.test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        sess.current_selected_file = self.file_name
        sess.current_selected_file_number = 1
        sess.dispatch_action(window, ord('v'))
        sess.draw(window)
        sess.perform_viewer_action(window, curses.KEY_UP)
        sess.perform_viewer_action(window, curses.KEY_UP)
        sess.perform_viewer_action(window, curses.KEY_UP)
        self.assertEqual(0, sess.current_position_in_file)

    def test_refresh_called_with_correct_args(self):
        sess = Hyaloclastite('filebrowser', self.test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        sess.current_selected_file = self.file_name
        sess.current_selected_file_number = 1
        sess.dispatch_action(window, ord('v'))
        sess.draw(window)
        sess.perform_viewer_action(window, curses.KEY_DOWN)
        sess.perform_viewer_action(window, curses.KEY_DOWN)
        sess.perform_viewer_action(window, curses.KEY_DOWN)
        sess.draw(window)
        self.assertEqual([3, 0, 0, 0, curses.LINES - 1, curses.COLS - 1], window.last_refresh_args)

