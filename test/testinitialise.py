#!/usr/bin/python

import unittest
import curses
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from classes.hyaloclastite import hyaloclastite

class TestViewer(unittest.TestCase):
    def test_create_session(self):
        sess = hyaloclastite(1,2,3)
        self.assertTrue(isinstance(sess,hyaloclastite))

    def test_fields_initialised(self):
        a = 'a'
        b = 'b'
        c = 'c'
        sess = hyaloclastite(a,b,c)
        self.assertEqual(sess.mainwin, a)
        self.assertEqual(sess.mode, b)
        self.assertEqual(sess.vault, c)

