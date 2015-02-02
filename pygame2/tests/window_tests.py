"""
"""
from unittest import TestCase, skip
from mock import patch, call
from logging import getLogger

from pygame2 import window

logger = getLogger()


class DisplayTests(TestCase):
    def setUp(self):
        self.window = window.WindowBase()

    # def test_init(self):
    # """init is a noop"""
    # self.assertIsNone(self.window.init())

    @skip("TODO: this test should target the pygame window provider only")
    @patch("pygame2.window.pyglet")
    def test_set_mode_initializes_display_singleton(self, mock_pyglet):
        """set_mode initializes the display singleton and pyglet main window"""
        res = (640, 480)
        surface = self.window.set_mode(res)
        self.assertIs(self.window.Window._instance, surface)
        self.assertEqual(self.window.Window._instance.get_resolution(), res)

        # make sure there can only be one instance of the display
        one = window.WindowBase(None)
        two = window.WindowBase(None)
        three = window.WindowBase(None)
        self.assertIs(one, two)
        self.assertIs(two, three)
        self.assertIs(one, three)
        self.assertTrue(mock_pyglet.window.Window.called)
        # self.assertIs(self.window.Window(None)._instance.window,
        #               mock_pyglet.window.Window.return_value)

    def test_set_caption(self):
        """can set the pyglet window caption on the
        singleton window instance"""
        title = "Zort: The Explorer"
        self.window.caption = title

    def test_get_caption(self):
        """can get the caption from the pyglet window"""
        self.window.caption = "foobar"
        self.assertEqual(self.window.caption, "foobar")

    def test_toggle_fullscreen(self):
        self.assertFalse(self.window.fullscreen)
        self.window.fullscreen = True
        self.assertTrue(self.window.fullscreen)
        self.window.fullscreen = False
        self.assertFalse(self.window.fullscreen)
        # expected = [call(True), call(False)]
        # window = mock_pyglet.window.Window.return_value
        # actual = self.window.set_fullscreen.call_args_list
        # self.assertEqual(expected, actual)

    @skip('Should only test the host layer')
    def test_flip(self):
        self.assertIsNone(self.window.flip())

    @skip("TODO: window.quit()?  should we lose this method?")
    @patch("pygame2.window.pyglet")
    def test_quit(self, mock_pyglet):
        self.window.set_mode((0, 0))
        self.assertIsNone(self.window.quit())
        self.assertIsNone(self.window.Window._instance)

    @skip("TODO: should target pyglet")
    @patch("pygame2.window.pyglet")
    def test_get_surface(self, mock_pyglet):
        self.assertIsNone(self.window.get_surface())
        screen = self.window.set_mode((0, 0))
        self.assertIs(screen, self.window.get_surface())

        # def test_quit(self):
        #     self.fail("test not implemented")

        # def test_get_init(self):
        #     self.fail("test not implemented")

        # def test_get_surface(self):
        #     self.fail("test not implemented")

        # def test_get_driver(self):
        #     self.fail("test not implemented")

        # def test_Info(self):
        #     self.fail("test not implemented")

        # def test_get_wm_info(self):
        #     self.fail("test not implemented")

        # def test_list_modes(self):
        #     self.fail("test not implemented")

        # def test_mode_ok(self):
        #     self.fail("test not implemented")

        # def test_gl_get_attribute(self):
        #     self.fail("test not implemented")

        # def test_gl_set_attribute(self):
        #     self.fail("test not implemented")

        # def test_get_active(self):
        #     self.fail("test not implemented")

        # def test_iconify(self):
        #     self.fail("test not implemented")

        # def test_toggle_fullscreen(self):
        #     self.fail("test not implemented")

        # def test_set_gamma(self):
        #     self.fail("test not implemented")

        # def test_set_gamma_ramp(self):
        #     self.fail("test not implemented")

        # def test_set_icon(self):
        #     self.fail("test not implemented")

        # def test_set_palette(self):
        #     self.fail("test not implemented")
