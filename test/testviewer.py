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
        for action in {'e'}:
            self.assertTrue(is_viewer_action_correct(action))

