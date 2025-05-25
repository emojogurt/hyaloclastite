#!/usr/bin/python

import unittest
import sys
from os import path, environ, remove

import fakeCurses

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from classes.hyaloclastite import Hyaloclastite

class TestViewerActions(unittest.TestCase):
    def setUp(self):
        self.base_directory = path.dirname(path.dirname(path.abspath(__file__)))
        self.parrot_file_location = path.join(self.base_directory, 'test', 'parrotargs.txt')
        self.test_location = path.join(self.base_directory, 'test', "testvault1")
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

        try:
            remove(self.parrot_file_location)
        except FileNotFoundError:
            pass

    def test_close_file_returns_to_filebrowser(self):
        sess = Hyaloclastite('filebrowser', self.test_location)
        window = fakeCurses.FakeWindow()
        sess.get_dir_contents()
        sess.current_selected_file = 'file2'
        sess.current_selected_file_number = 2
        sess.dispatch_action(window, ord('v'))
        self.assertEqual('viewer', sess.mode)
        sess.perform_viewer_action(window, ord('c')) # TODO - allow for customised controls, no hardcoded values
        self.assertEqual('filebrowser', sess.mode)

    def test_editor_called_with_params_from_viewer(self):
        environ['EDITOR'] = "./parrot.py"

        file2_location = path.join(self.base_directory, 'test', "testvault1", "file2")
        with open(self.parrot_file_location, 'w') as parrot_file:
            parrot_file.write('test')
        sess = Hyaloclastite('filebrowser', self.test_location)
        window = fakeCurses.FakeWindow()
        sess.current_selected_file = 'file2'

        sess.perform_viewer_action(window, ord('e'))

        with open(self.parrot_file_location, 'r') as parrot_file:
            content = parrot_file.read()
        expected_content = "['" + str(path.abspath(file2_location)) + "']"
        self.assertEqual(expected_content, content)
