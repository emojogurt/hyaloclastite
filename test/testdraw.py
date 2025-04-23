#!/usr/bin/python

import unittest
import sys
from os import path

import fakeCurses

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from classes.hyaloclastite import Hyaloclastite

class TestDraw(unittest.TestCase):
    def test_draw_random_stuff(self):
        sess = Hyaloclastite(1, 2)
        sess.current_screen_contents = "test contents"
        window = fakeCurses.WindowFakePrint()
        sess.draw(window)
        self.assertEqual("test contents", window.text)
        self.assertTrue(window.called_clear)
        self.assertTrue(window.called_refresh)


