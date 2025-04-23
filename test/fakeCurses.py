#!/usr/bin/python

class WindowReturnChar:
    def __init__(self, retchar):
        self.retchar = retchar
    def getch(self):
        return self.retchar

class WindowFakePrint:
    def __init__(self):
        self.text = None
        self.prepared = None
        self.called_clear = False
        self.called_refresh = False
    def clear(self):
        self.called_clear = True
    def refresh(self):
        self.called_refresh = True
        self.text = self.prepared
    def addstr(self, text):
        self.prepared = text
