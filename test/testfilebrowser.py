#!/usr/bin/python

import unittest
import sys
from os import path

import fakeCurses
import curses

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from classes.hyaloclastite import Hyaloclastite

class TestFilebrowser(unittest.TestCase):
    def test_get_known_dir_contents(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        sess.get_dir_contents()
        contents = list(fsobject.name for fsobject in sess.current_directory_listing.values())
        self.assertIn('directory1', contents)
        self.assertIn('file1', contents)
        self.assertIn('file2', contents)

    def test_first_entry_selected_at_entry(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        sess.get_dir_contents()
        self.assertEqual('directory1', sess.current_selected_file)

    def test_window_draw(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.WindowFakePrint()
        sess.start()
        sess.draw(window)
        self.assertTrue(window.called_clear)
        self.assertTrue(window.called_refresh)
    
    def test_correct_file_list_displayed(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.WindowFakePrint()
        sess.start()
        sess.draw(window)
        self.assertEqual("testvault1\n directory1\n file1\n file2", window.gettext())

    def test_directories_are_bolded(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.WindowFakePrint()
        sess.start()
        sess.draw(window)
        self.assertEqual(curses.A_BOLD, curses.A_BOLD & window.text['\n directory1'][0])

    def test_selection_is_reversed_startup(self):
        # at start time first entry is selected
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.WindowFakePrint()
        sess.start()
        sess.draw(window)
        self.assertEqual(curses.A_REVERSE, curses.A_REVERSE & window.text['\n directory1'][0])
    
    def test_selection_is_reversed_other(self):
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', "testvault1")
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.WindowFakePrint()
        sess.start()
        sess.current_selected_file = 'file1'
        sess.draw(window)
        self.assertEqual(curses.A_REVERSE, curses.A_REVERSE & window.text['\n file1'][0])



