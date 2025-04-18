#!/usr/bin/python

import unittest
import sys
from os import path
from unittest import mock

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from classes.hyaloclastite import hyaloclastite
import fakeCurses

class TestQuit(unittest.TestCase):
    def setUp(self):
        self.testsession = hyaloclastite('filebrowser', '.')

    def test_quit_program(self):
        window = fakeCurses.windowretchar(ord('q'))
        self.assertEqual(0, self.testsession.main(window,2,3))
