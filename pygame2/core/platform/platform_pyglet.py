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
fork pyglet and use pyglet's excellent ctypes-based OS interfaces and
then handle the queue directly.
"""
from functools import partial

import pyglet
import pyglet.app

from pygame2.event import PlatformEventQueueBase
from pygame2.window import WindowBase


__all__ = ('PlatformEventQueue', 'Window')


def patch_pyglet_events(dispatcher, pyglet_dispatcher):
    """Collect all events from the window class, bind them, then
    set up a dispatcher for them.
    """
    # TDOD: figure some way to reconcile pygame2's no argument dispatch
    # and pyglets multiple argument/kwarg dispatch
    def dispatch(name, *args, **kwargs):
        kwargs['args'] = args
        dispatcher.broadcast(name, **kwargs)

    for event_name in pyglet_dispatcher.event_types:
        if not hasattr(dispatcher, event_name):
            try:
                dispatcher.register(event_name)
            except dispatcher.DuplicateEventName:
                continue
            func = partial(dispatch, event_name)
            setattr(pyglet_dispatcher, event_name, func)


class PlatformEventQueue(PlatformEventQueueBase):
    """ Pyglet based event queue
    """

    def exit_blocking(self):
        pass

    def _blocking_timer(self):
        pass

    def enter_blocking(self):
        pass

    def start(self):
        self.platform_event_loop = pyglet.app.platform_event_loop
        self.platform_event_loop.start()

    def get(self, event_filter=None):
        timeout = .005
        self.platform_event_loop.notify()
        self.platform_event_loop.step(timeout)
        # sleep isn't implemented on os x, yet
        # self.platform_event_loop.sleep(30)

    def post(self, event):
        pass

    def stop(self):
        pass

    def poll(self):
        pass

    def clear(self, event_filter=None):
        pass

    def peek(self, types=None):
        pass


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

        # connect pyglet dispatcher to pygame2 dispatcher
        # an unpleasant side effect is that arguments passed
        # to pyglet events are lost.  this will change.
        patch_pyglet_events(self, self._window)

        # temp setup
        self._window.switch_to()
        self._window.dispatch_pending_events()
        self._window.dispatch_events()

    def close(self):
        pass

    def activate(self):
        pass

    def flip(self):
        self._window.flip()

    def switch_to(self):
        self._window.switch_to()

    def dispatch_pending_events(self):
        """ Pyglet provides an event queue for each window

        TODO: remove this once event queue is finalized

        :return: None
        """
        self._window.dispatch_pending_events()

    def minimize(self):
        pass

    def maximize(self):
        pass
