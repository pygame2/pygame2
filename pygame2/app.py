"""pygame2 app

* contains event loop
* dispatches events
* reads input
* manages audio
* has clock/scheduler
* handles screen/window/display updating
* loads shaders, opengl programs, etc
"""
import time

import pygame2
from pygame2.event import EventDispatcher

__all__ = ('App', )


class App(EventDispatcher):

    __events__ = ('on_enter', 'on_close', 'on_exit')

    def __init__(self):
        super().__init__()
        self.clock = pygame2.clock.Clock()
        self.running = False
        self.windows = list()

    def start(self):
        if self.running:
            print('App.start called twice')
            raise RuntimeError

        self.running = True
        self.broadcast('on_enter')

    def run(self):
        """
        send start event
        manage event loop
        """
        self.start()

        # get our events from the platform
        platform_queue = pygame2.core.platform.get_platform_event_queue()
        platform_queue.start()

        # TODO: address the run method when adding support for multiple windows
        try:
            window = self.windows[0]
        except IndexError:
            print('create a window before calling App.run')
            raise RuntimeError

        window.subscribe('on_close', self.stop)

        while self.running:
            self.clock.tick()

            platform_queue.get()

            window.switch_to()

            # TODO: aggrigate pyglet/window events into our monolithic queue

            # pyglet windows maintain their own queue of events
            # this method tells the window to dispatch any events in its queue
            window.dispatch_pending_events()
            window.broadcast('on_draw')
            window.flip()

            # TODO: make sure we can sleep correctly on all platforms
            # sleep_time = self.clock.get_idle_time()
            time.sleep(.015)

        self.broadcast('on_exit')

    def stop(self):
        self.running = False

    def create_window(self, *args, **kwargs):
        window = pygame2.core.platform.create_window(**kwargs)
        self.windows.append(window)
        return window

