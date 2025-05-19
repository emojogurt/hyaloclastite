#!/usr/bin/python

class FakeWindow:
    def __init__(self):
        self.text = None
        self.prepared = {}
        self.called_clear = False
        self.called_refresh = False
        self.retchar = None
        self.window_COLS = 0
        self.window_LINES = 0
        self.shouldileaveok = None
        self.last_refresh_args = None

    def set_retchar(self, retchar):
        self.retchar = retchar
    def resize(self, lines, cols):
        self.window_LINES = lines
        self.window_COLS = cols
    def clear(self):
        self.called_clear = True
    def refresh(self, pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol):
        self.called_refresh = True
        self.text = self.prepared
        self.last_refresh_args = [pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol]
    def addstr(self, text, *args):
        self.prepared[text] = args
    def getmaxyx(self):
        return self.window_LINES, self.window_COLS
    def gettext(self):
        return "".join(list(self.text.keys()))
    def getch(self):
        return self.retchar
    def leaveok(self, shouldi):
        self.shouldileaveok = shouldi
