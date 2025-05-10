#!/usr/bin/python

import unittest
import sys
from os import path, environ

import fakeCurses

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from classes.hyaloclastite import Hyaloclastite

class TestViewerActions(unittest.TestCase):
    def setUp(self):
        try:
            self.origvalue = environ['EDITOR']
        except KeyError:
            self.origvalue = None

    def tearDown(self):
        if self.origvalue is None:
            try:
                del environ['EDITOR']
            except KeyError:
                pass
        else:
            environ['EDITOR'] = self.origvalue

    def test_close_file_returns_to_filebrowser(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        sess.current_selected_file = 'file2'
        sess.current_selected_file_number = 2
        sess.dispatch_action(window, ord('v'))
        self.assertEqual('viewer', sess.mode)
        sess.perform_viewer_action(window, ord('c')) # TODO - allow for customised controls, no hardcoded values
        self.assertEqual('filebrowser', sess.mode)


