#!/usr/bin/python

import unittest
import sys
from os import path
from unittest import mock

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from classes.hyaloclastite import Hyaloclastite
from test import fakeCurses

class TestQuit(unittest.TestCase):
    def setUp(self):
        self.test_session = Hyaloclastite('filebrowser', '.')

    def test_quit_program(self):
        window = fakeCurses.WindowReturnChar(ord('q'))
        self.assertEqual(0, self.test_session.main(window, 2, 3))
