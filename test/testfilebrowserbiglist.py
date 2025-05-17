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
        genfilename = 'a_file'
        self.dirname = "testvault_generated"
        os.mkdir(self.dirname)
        with open(os.path.join(self.dirname,file1name), 'w') as file1:
            file1.write('test')

        for fnum in range(1,498):
            fname = genfilename + str(fnum)
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
        test_location = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'test', self.dirname)
        sess = Hyaloclastite('filebrowser', test_location)
        window = fakeCurses.FakeWindow()
        sess.start()
        sess.draw(window)
        self.assertEqual(500, window.window_LINES)
        self.assertEqual(255, window.window_COLS)
