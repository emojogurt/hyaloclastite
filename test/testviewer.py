#!/usr/bin/python

import unittest
import curses
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from functions.vieweractions import is_viewer_action_correct

class TestViewer(unittest.TestCase):
#    def setUp(self):

#    def tearDown(self):

    def test_is_viewer_action_correct_positive(self):
        for action in {ord('e'), curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_HOME, curses.KEY_END}:
            self.assertTrue(is_viewer_action_correct(action))


    def test_is_viewer_action_correct_negative(self):
        for action in {ord('z'), curses.KEY_BACKSPACE, ord('4')}:
            self.assertFalse(is_viewer_action_correct(action))
            self.assertIsNotNone(is_viewer_action_correct(action))
