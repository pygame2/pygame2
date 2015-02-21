"""
Pyglet based platform

Pyglet is a cross-platform multimedia library built with python
and ctypes.  It is a good target for Windows, Mac, and Linux,
but may be slower on pypy.
"""
from pygame2.window import WindowBase
from pygame2.event import PlatformEventQueueBase
import pyglet
import pyglet.app


class PlatformEventQueue(PlatformEventQueueBase):
    """ Pyglet based event queue
    """

    def start(self):
        self.platform_event_loop = pyglet.app.platform_event_loop
        self.platform_event_loop.start()

    def get(self, event_filter=None):
        timeout = .1
        self.platform_event_loop.notify()
        self.platform_event_loop.step(timeout)
        # sleep isn't implemented on os x, yet
        # self.platform_event_loop.sleep(30)


class Window(WindowBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        width, height = kwargs.get('size', (0, 0))

        kw = {
            'width': width,
            'height': height,
            'caption': self._caption,
            'resizable': self._resizable,
            'fullscreen': self._fullscreen,
            'visible': self._visible,
            'vsync': self._vsync,
        }

        self._window = pyglet.window.Window(**kw)

        # temp setup
        self._window.switch_to()
        self._window.dispatch_pending_events()
        self._window.dispatch_events()

    def flip(self):
        self._window.flip()

    def switch_to(self):
        self._window.switch_to()
