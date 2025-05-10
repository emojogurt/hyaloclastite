#!/usr/bin/python

import unittest
import sys
from os import path, environ

import fakeCurses
import curses

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from classes.hyaloclastite import Hyaloclastite

class TestFilebrowserActions(unittest.TestCase):
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


    def test_down_arrow_selects_next(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        sess.dispatch_action(window,curses.KEY_DOWN)
        sess.draw(window)
        self.assertEqual(1, sess.current_selected_file_number)
        self.assertEqual(curses.A_REVERSE, curses.A_REVERSE & window.text['\n file1'][0])

    def test_no_down_movement_from_last(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        sess.current_selected_file = 'file2'
        sess.current_selected_file_number = 2
        sess.dispatch_action(window, curses.KEY_DOWN)
        sess.draw(window)
        self.assertEqual(2, sess.current_selected_file_number)
        self.assertEqual(curses.A_REVERSE, curses.A_REVERSE & window.text['\n file2'][0])

    def test_up_arrow_selects_previous(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        sess.current_selected_file = 'file2'
        sess.current_selected_file_number = 2
        sess.dispatch_action(window, curses.KEY_UP)
        sess.draw(window)
        self.assertEqual(1, sess.current_selected_file_number)
        self.assertEqual(curses.A_REVERSE, curses.A_REVERSE & window.text['\n file1'][0])

    def test_no_up_movement_from_first(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        sess.dispatch_action(window,curses.KEY_UP)
        sess.draw(window)
        self.assertEqual(0, sess.current_selected_file_number)
        self.assertEqual(curses.A_REVERSE, curses.A_REVERSE & window.text['\n directory1'][0])

    def test_change_mode_to_view(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        sess.current_selected_file = 'file1'
        sess.current_selected_file_number = 1
        sess.dispatch_action(window, ord('v'))
        self.assertEqual('viewer', sess.mode)

    def test_editor_called_with_params_from_filebrowser(self):
        environ['EDITOR'] = "./parrot.py"
        base_directory = path.dirname(path.dirname(path.abspath(__file__)))
        parrot_file_location = path.join(base_directory, 'test', 'parrotargs.txt')
        test_location = path.join(base_directory, 'test', "testvault1")
        file2_location = path.join(base_directory, 'test', "testvault1", "file2")
        with open(parrot_file_location, 'w') as parrot_file:
            parrot_file.write('test')
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        sess.current_selected_file = 'file2'
        sess.current_selected_file_number = 2
        sess.perform_filebrowser_action(window, ord('e'))

        with open(parrot_file_location, 'r') as parrot_file:
            content = parrot_file.read()
        expected_content = "['" + str(path.abspath(file2_location)) + "']"
        self.assertEqual(expected_content, content)