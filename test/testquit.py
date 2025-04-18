#!/usr/bin/python

import unittest
import curses
import sys
from os import path
from unittest import mock

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from classes.hyaloclastite import hyaloclastite

class TestQuit(unittest.TestCase):
    def test_quit_program(self):
        with mock.MagicMock(__main__.exit, )
