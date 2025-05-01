#!/usr/bin/python

import unittest
import sys
from os import path

import fakeCurses
import curses

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from classes.hyaloclastite import Hyaloclastite

class TestFilebrowser(unittest.TestCase):
    def test_down_arrow_selects_next(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.WindowFakePrint()
        sess.start()
        sess.perform_filebrowser_action(window,curses.KEY_DOWN)
        sess.draw(window)
        self.assertEqual(1, sess.current_selected_file_number)
        self.assertEqual(curses.A_REVERSE, curses.A_REVERSE & window.text['\n file1'][0])

    def test_no_down_movement_from_last(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.WindowFakePrint()
        sess.start()
        sess.current_selected_file = 'file2'
        sess.current_selected_file_number = 2
        sess.perform_filebrowser_action(window, curses.KEY_DOWN)
        sess.draw(window)
        self.assertEqual(2, sess.current_selected_file_number)
        self.assertEqual(curses.A_REVERSE, curses.A_REVERSE & window.text['\n file2'][0])

    def test_up_arrow_selects_previous(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.WindowFakePrint()
        sess.start()
        sess.current_selected_file = 'file2'
        sess.current_selected_file_number = 2
        sess.perform_filebrowser_action(window, curses.KEY_UP)
        sess.draw(window)
        self.assertEqual(1, sess.current_selected_file_number)
        self.assertEqual(curses.A_REVERSE, curses.A_REVERSE & window.text['\n file1'][0])

    def test_no_up_movement_from_first(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.WindowFakePrint()
        sess.start()
        sess.perform_filebrowser_action(window,curses.KEY_UP)
        sess.draw(window)
        self.assertEqual(0, sess.current_selected_file_number)
        self.assertEqual(curses.A_REVERSE, curses.A_REVERSE & window.text['\n directory1'][0])
