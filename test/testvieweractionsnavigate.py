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
            file1.write('test')

        with open(path.join(self.test_location, self.file_name), 'a') as genfile:
            for line_num in range(1, curses.LINES + 50):
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
        sess.perform_viewer_action(window, curses.KEY_DOWN)
        self.assertEqual(sess.current_position_in_file, 1)

    def test_uparrow_scrolls_up(self):
        sess = Hyaloclastite('filebrowser', self.test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        sess.current_selected_file = self.file_name
        sess.current_selected_file_number = 1
        sess.dispatch_action(window, ord('v'))
        sess.current_position_in_file = 3
        sess.perform_viewer_action(window, curses.KEY_UP)
        self.assertEqual(sess.current_position_in_file, 2)




