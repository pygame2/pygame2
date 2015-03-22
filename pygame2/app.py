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
    def __init__(self):
        super().__init__()
        self.clock = pygame2.clock.Clock()
        self.running = False
        self.windows = list()

    def start(self):
        self.dispatch('app_start')
        self.running = True

    def run(self, window):
        """
        create window
        set window title
        set window/app icon
        send start event
        manage event loop
        """
        self.start()

        queue = pygame2.core.platform.get_platform_event_queue()
        queue.start()

        window.bind('on_close', self.stop)

        while self.running:
            self.clock.tick()

            # get our events from the platform
            queue.get()

            window.switch_to()
            window.dispatch_pending_events()
            window.dispatch('on_draw')
            window.flip()

            # TODO: make sure we can sleep correctly on all systems
            # sleep_time = self.clock.get_idle_time()
            time.sleep(.015)

    def stop(self):
        self.running = False

    def create_window(self, *args, **kwargs):
        window = pygame2.core.platform.create_window(**kwargs)
        self.windows.append(window)
        return window

