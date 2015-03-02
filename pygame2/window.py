"""
Abstract Hierarchy of Window Concepts:

'display', basically this is the gpu
'screen', could be the is a logical screen on one monitor or more
'window', as is
'canvas', drawing context for graphics.  could be a pygame surface, could be
          and opengl buffer
"""
from pygame2.core import core_modules
from pygame2.event import EventDispatcher
import pygame2

core_modules['window'] = ('window_pyglet', 'window_pygame')


class WindowBase(EventDispatcher):
    """Platform independent window
    """
    _resolution = None
    _fullscreen = False
    _caption = None
    _resizable = False
    _borderless = False
    _minimized = False
    _maximized = False
    _visible = True
    _vsync = True
    _screen = None

    # stored to remember size when toggling fullscreen
    _window_rect = None

    # if true, then the window will be be redrawn at next opportunity.
    # to limit drawing, you can set to false to prevent draws until it
    # is needed, then set to true
    requires_draw = True

    _default_size = 640, 480

    def __init__(self, **kwargs):
        super().__init__()

        # scan keyword arguments and set values in our instance
        # to match, but only if they are defined by WindowBase
        for name, value in kwargs.items():
            if hasattr(self, name):
                setattr(self, name, value)

        if self._resolution is None:
            self._resolution = WindowBase._default_size

            # TODO: keep a list of active windows somewhere

            # self.switch_to()
            # if self._visible:
            # self.activate

    def get_resolution(self):
        return self._resolution

    def get_size(self):
        return self._resolution

    @property
    def fullscreen(self):
        return self._fullscreen

    @fullscreen.setter
    def fullscreen(self, value):
        if not value == self._fullscreen:
            self._fullscreen = value

    @property
    def height(self):
        return self._resolution[1]

    @property
    def width(self):
        return self._resolution[0]

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, value):
        if not value == self._caption:
            self._caption = value

    def activate(self):
        """Force window to get/steal focus.

        Actual behavior depends on OS
        """
        raise NotImplementedError

    def get_rect(self):
        return pygame2.Rect((0, 0), self._resolution)

    def dispatch_events(self):
        """Poll the operating system event queue for new events and call
        attached event handlers.

        Typical applications should use `pygame2.app.App`.
        """
        raise NotImplementedError('abstract')

    def create_renderer(self):
        """ Return a new renderer (sprite group) that draws to this window
        """
        raise NotImplementedError

    def flip(self):
        """flip, etc"""
        raise NotImplementedError

    def switch_to(self):
        """Make window current OpenGL rendering context
        """
        raise NotImplementedError
