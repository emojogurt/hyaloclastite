#!/usr/bin/python
import curses
import unittest
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from classes.hyaloclastite import Hyaloclastite
import fakeCurses

class TestQuit(unittest.TestCase):
    def setUp(self):
        self.test_session = Hyaloclastite('filebrowser', '.')
        curses.initscr()

    def tearDown(self):
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def test_quit_program(self):
        window = fakeCurses.FakeWindow()
        window.set_retchar(ord('q'))
        self.assertEqual(0, self.test_session.main(window, 2, 3))
