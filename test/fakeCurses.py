#!/usr/bin/python

class WindowReturnChar:
    def __init__(self, retchar):
        self.retchar = retchar
    def clear(self):
        pass
    def addstr(self, text):
        pass
    def refresh(self):
        pass
    def getch(self):
        return self.retchar

class WindowFakePrint:
    def __init__(self):
        self.text = None
        self.prepared = {}
        self.called_clear = False
        self.called_refresh = False
    def clear(self):
        self.called_clear = True
    def refresh(self):
        self.called_refresh = True
        self.text = self.prepared
    def addstr(self, text, *args):
        self.prepared[text] = args

    def gettext(self):
        return "".join(list(self.text.keys()))
