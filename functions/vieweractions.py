#!/usr/bin/python
import curses

def is_viewer_regular_action(action):
    if action in {ord('e'), curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_HOME, curses.KEY_END}:
        return True
    else:
        return False