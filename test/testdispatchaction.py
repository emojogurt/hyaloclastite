import unittest
import sys
from os import path
from unittest import mock

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from classes.hyaloclastite import Hyaloclastite, IncorrectModeException


class TestDispatchAction(unittest.TestCase):
    def test_erroneous_mode(self):
        sess = Hyaloclastite('incorrect', '/path')
        self.assertRaises(IncorrectModeException, sess.dispatch_action, 'window', 'e')

    def test_dispatch_filebrowser(self):
        sess = Hyaloclastite('filebrowser', '.')
        with mock.patch('classes.hyaloclastite.Hyaloclastite.perform_filebrowser_action') as fake_perform_fb_a:
            sess.dispatch_action('window', ord('e'))
            fake_perform_fb_a.assert_called_once_with('window', ord('e'))

    def test_dispatch_viewer(self):
        sess = Hyaloclastite('viewer', '.')
        with mock.patch('classes.hyaloclastite.Hyaloclastite.perform_viewer_action') as fake_perform_fb_a:
            sess.dispatch_action('window', ord('e'))
            fake_perform_fb_a.assert_called_once_with('window', ord('e'))