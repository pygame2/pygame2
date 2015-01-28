"""
Abstract Hierarchy of Window Concepts:

'display', basically this is the gpu
'screen', could be the is a logical screen on one monitor or more
'window', as is
'canvas', drawing context for graphics.  could be a pygame surface, could be
          and opengl buffer
"""
import pygame2


class Window:
    def __init__(self, resolution=None, flags=0, depth=0):
        self._fullscreen = False
        self._caption = "pygame too"
        if resolution is None:
            resolution = (640, 480)
        self.resolution = resolution
        self.flags = flags
        self.depth = depth

    def get_resolution(self):
        return self.resolution

    def get_size(self):
        return self.resolution

    @property
    def fullscreen(self):
        return self._fullscreen

    @fullscreen.setter
    def fullscreen(self, value):
        if not value == self._fullscreen:
            self._fullscreen = value

    @property
    def height(self):
        return self.resolution[1]

    @property
    def width(self):
        return self.resolution[0]

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, value):
        if not value == self._caption:
            self._caption = value

    def get_rect(self):
        return pygame2.Rect((0, 0), self.resolution)

    def create_renderer(self):
        """ Return a new renderer (sprite group) that draws to this window
        """
        pass

    def flip(self):
        """flip, etc"""
        pass
