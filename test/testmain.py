#!/usr/bin/python

import unittest
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from classes.hyaloclastite import Hyaloclastite

class TestMain(unittest.TestCase):
    def test_get_dir_contents_at_filebrowser_startup(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        sess.get_dir_contents()
        self.assertIn('directory1', list(sess.current_directory_listing.keys()))
        self.assertIn('file1', list(sess.current_directory_listing.keys()))
        self.assertIn('file2', list(sess.current_directory_listing.keys()))
