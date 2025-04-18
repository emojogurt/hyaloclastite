#!/usr/bin/python

import unittest
import curses
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from classes.hyaloclastite import hyaloclastite

class TestInitialise(unittest.TestCase):
    def test_create_session(self):
        sess = hyaloclastite(1,2)
        self.assertTrue(isinstance(sess,hyaloclastite))

    def test_fields_initialised(self):
        a = 'a'
        b = 'b'
        sess = hyaloclastite(a,b)
        self.assertEqual(sess.mode, a)
        self.assertEqual(sess.vault, b)

