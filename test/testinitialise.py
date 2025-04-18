#!/usr/bin/python

import unittest
import curses
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from classes.hyaloclastite import Hyaloclastite

class TestInitialise(unittest.TestCase):
    def test_create_session(self):
        sess = Hyaloclastite(1, 2)
        self.assertTrue(isinstance(sess, Hyaloclastite))

    def test_fields_initialised(self):
        a = 'a'
        b = 'b'
        sess = Hyaloclastite(a, b)
        self.assertEqual(sess.mode, a)
        self.assertEqual(sess.vault, b)

