#!/usr/bin/python

import unittest
import sys
from os import path, environ

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import fakeCurses

from classes.hyaloclastite import Hyaloclastite

class TestQuit(unittest.TestCase):
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

    def test_launch_editor(self):
        environ['EDITOR'] = "./write_something.py"
        base_directory = path.dirname(path.dirname(path.abspath(__file__)))
        something_file_location = path.join(base_directory, 'test', 'filewithsomething.txt')
        test_location = path.join(base_directory, 'test', "testvault1")
        with open(something_file_location, 'w') as file_with_something:
            file_with_something.write('test')
        sess = Hyaloclastite('filebrowser', test_location)
        sess.start()
        sess.current_selected_file = 'file2'
        sess.current_selected_file_number = 2
        sess.launch_editor()

        with open(something_file_location, 'r') as file_with_something:
            content = file_with_something.read()
        expected_content = "something"
        self.assertEqual(expected_content, content)
