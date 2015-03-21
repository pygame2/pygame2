"""
Pyglet based platform

Pyglet is a cross-platform multimedia library built with python
and ctypes.  It is a good target for Windows, Mac, and Linux,
but may be slower on pypy.

pyglet is almost a pure event oriented framework, so the way pygame2
handles it will seem awkward:
   - set event handlers for each input
   - catch events and queue them

if we are to remove this queue/dequeue steps, then we'll have to
fork pyglet and use pyglet's excellet ctypes-based OS interfaces and
then handle the queue directly.
"""
import pyglet
import pyglet.app

from pygame2.event import PlatformEventQueueBase
from pygame2.window import WindowBase

# from pygame2.input.keyboard import KeyboardBase
# from pygame2.input.mouse import MouseBase


__all__ = ('PlatformEventQueue', 'Window')


class PlatformEventQueue(PlatformEventQueueBase):
    """ Pyglet based event queue
    """

    def start(self):
        self.platform_event_loop = pyglet.app.platform_event_loop
        self.platform_event_loop.start()

    def get(self, event_filter=None):
        timeout = .001
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

    def dispatch_pending_events(self):
        """ Pyglet provides an event queue for each window

        :return: None
        """
        queue = self._window._event_queue
        while queue:
            event = queue.pop(0)
            if type(event[0]) is str:
                self.dispatch(event[0])
            else:
                # win32 event
                event[0](*event[1:])
