#!/usr/bin/python

import unittest
import sys
from os import path, environ, remove

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from classes.hyaloclastite import Hyaloclastite

class TestQuit(unittest.TestCase):
    def setUp(self):
        self.base_directory = path.dirname(path.dirname(path.abspath(__file__)))
        self.something_file_location = path.join(self.base_directory, 'test', 'filewithsomething.txt')
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
            remove(self.something_file_location)
        except FileNotFoundError:
            pass

    def test_launch_editor_filebrowser(self):
        environ['EDITOR'] = "./write_something.py"

        with open(self.something_file_location, 'w') as file_with_something:
            file_with_something.write('test')
        sess = Hyaloclastite('filebrowser', self.test_location)
        sess.get_dir_contents()
        # note: something is selected here, but it doesn't really matter
        # the "editor" here is simply a program that writes a hardcoded value to a hardcoded path
        sess.current_selected_file = 'file2'
        sess.current_selected_file_number = 2
        sess.launch_editor()

        with open(self.something_file_location, 'r') as file_with_something:
            content = file_with_something.read()
        expected_content = "something"
        self.assertEqual(expected_content, content)
