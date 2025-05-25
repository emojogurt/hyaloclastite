#!/usr/bin/python
import os
import unittest
import sys
from os import path

import fakeCurses
import curses

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from classes.hyaloclastite import Hyaloclastite

class TestFilebrowser(unittest.TestCase):
    def setUp(self):
        curses.initscr()
        file1name = 'a'*254
        self.genfilename = 'a_file'
        self.dirname = "testvault_generated"
        os.mkdir(self.dirname)
        self.test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', self.dirname)
        with open(os.path.join(self.dirname,file1name), 'w') as file1:
            file1.write('test')

        for fnum in range(1,498):
            fname = self.genfilename + str(fnum)
            with open(os.path.join(self.dirname, fname), 'w') as genfile:
                genfile.write('a')

    def tearDown(self):
        for filename in os.listdir(self.dirname):
            os.remove(os.path.join(self.dirname,filename))
        os.removedirs(self.dirname)

        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def test_pad_resized_to_listing(self):
        sess = Hyaloclastite('filebrowser', self.test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        sess.draw(window)
        self.assertEqual(500, window.window_LINES)
        self.assertEqual(255, window.window_COLS)

    def test_move_page_at_bottom(self):
        sess = Hyaloclastite('filebrowser', self.test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        # assumption - at least 4 lines in the test window
        highlighted_before_name = self.genfilename + str(curses.LINES - 3)
        sess.current_selected_file = highlighted_before_name
        sess.current_selected_file_number = curses.LINES - 2 # one greater because of the first file being 'a'*254
        sess.dispatch_action(window, '0')
        sess.dispatch_action(window,curses.KEY_DOWN)
        sess.draw(window)
        self.assertEqual([curses.LINES, 0, 0, 0, curses.LINES - 1, curses.COLS - 1], window.last_refresh_args)

    def test_move_page_at_bottom_next_page(self):
        sess = Hyaloclastite('filebrowser', self.test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        # assumption - at least 4 lines in the test window
        highlighted_before_name = self.genfilename + str(curses.LINES * 2 - 3)
        sess.current_selected_file = highlighted_before_name
        sess.current_selected_file_number = curses.LINES * 2 - 2 # one greater because of the first file being 'a'*254
        sess.dispatch_action(window, '0')
        sess.dispatch_action(window,curses.KEY_DOWN)
        sess.draw(window)
        self.assertEqual([curses.LINES * 2, 0, 0, 0, curses.LINES - 1, curses.COLS - 1], window.last_refresh_args)

    def test_move_page_at_top(self):
        sess = Hyaloclastite('filebrowser', self.test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        # assumption - at least 4 lines in the test window
        highlighted_before_name = self.genfilename + str(curses.LINES - 2)
        sess.current_selected_file = highlighted_before_name
        sess.current_selected_file_number = curses.LINES - 1 # one greater because of the first file being 'a'*254
        sess.dispatch_action(window,'0') # empty action to scroll down first
        sess.dispatch_action(window,curses.KEY_UP)
        sess.draw(window)
        self.assertEqual([0, 0, 0, 0, curses.LINES - 1, curses.COLS - 1], window.last_refresh_args)

    def test_move_page_at_top_next_page(self):
        sess = Hyaloclastite('filebrowser', self.test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        # assumption - at least 4 lines in the test window
        highlighted_before_name = self.genfilename + str(curses.LINES * 2 - 2)
        sess.current_selected_file = highlighted_before_name
        sess.current_selected_file_number = curses.LINES * 2 - 1 # one greater because of the first file being 'a'*254
        sess.dispatch_action(window, '0')
        sess.dispatch_action(window,curses.KEY_UP)
        sess.draw(window)
        self.assertEqual([curses.LINES, 0, 0, 0, curses.LINES - 1, curses.COLS - 1], window.last_refresh_args)