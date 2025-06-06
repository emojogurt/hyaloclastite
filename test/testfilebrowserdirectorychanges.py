#!/usr/bin/python

import unittest
import sys
from os import path, environ, remove

import fakeCurses
import curses

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from classes.hyaloclastite import Hyaloclastite

class TestFilebrowserActions(unittest.TestCase):
    def setUp(self):
        curses.initscr()

    def tearDown(self):
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def test_enter_a_subdirectory(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.FakeWindow()
        sess.get_dir_contents()
        sess.current_selected_file_number = 0 # directory 1
        sess.dispatch_action(window, ord('v'))
        sess.draw(window)
        self.assertEqual("testvault1/directory1\n ..\n file3", window.gettext())

    def test_enter_a_deeper_subdirectory(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault4")
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.FakeWindow()
        sess.get_dir_contents()
        sess.dispatch_action(window, ord('v'))
        sess.draw(window)
        sess.current_selected_file_number = 1 # subdirectory1
        sess.dispatch_action(window, ord('v'))
        sess.draw(window)
        self.assertEqual("testvault4/subdirectory1\n ..\n file1", window.gettext())

    def test_up_one_level_selected(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.FakeWindow()
        sess.get_dir_contents()
        sess.current_selected_file_number = 0 # directory1
        sess.dispatch_action(window, ord('v'))
        sess.draw(window)
        self.assertEqual(curses.A_REVERSE, curses.A_REVERSE & window.text['\n ..'][0])

    def test_return_from_a_subdirectory(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault4")
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.FakeWindow()
        sess.get_dir_contents()
        sess.current_selected_file_number = 0 # directory1
        sess.dispatch_action(window, ord('v'))
        sess.draw(window)
        sess.current_selected_file_number = 1 # subdirectory1
        sess.dispatch_action(window, ord('v'))
        sess.draw(window)
        sess.current_selected_file_number = 0 # .. - up one level
        sess.dispatch_action(window, ord('v'))
        sess.draw(window)
        self.assertEqual("testvault4/directory1\n ..\n subdirectory1", window.gettext())