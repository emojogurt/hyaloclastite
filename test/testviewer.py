#!/usr/bin/python

import unittest
import sys
from os import path

import fakeCurses
import curses

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from classes.hyaloclastite import Hyaloclastite

class TestViewer(unittest.TestCase):
    def setUp(self):
        curses.initscr()

    def test_window_draw(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        sess.current_selected_file = 'file1'
        sess.current_selected_file_number = 1
        sess.dispatch_action(window, ord('v'))
        sess.draw(window)
        self.assertTrue(window.called_clear)
        self.assertTrue(window.called_refresh)
    
    def test_correct_file_contents_displayed(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        sess.current_selected_file = 'file1'
        sess.current_selected_file_number = 1
        sess.dispatch_action(window, ord('v'))
        sess.draw(window)
        self.assertEqual("file1\ntest content\nof file 1\nnothing to see here", window.gettext())

    def test_contents_longer_than_screen_no_exception(self):
        # note - file is 22 lines long, but we also always draw the header, which makes overall content 23 lines
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        window = curses.newpad(4,4)
        sess.start()
        sess.current_selected_file = 'file2'
        sess.current_selected_file_number = 2
        sess.dispatch_action(window, ord('v'))
        sess.draw(window)
