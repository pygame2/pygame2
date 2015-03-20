"""pygame2 app

* contains event loop
* dispatches events
* reads input
* manages audio
* has clock/scheduler
* handles screen/window/display updating
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

    def run(self, window):
        """
        create window
        set window title
        set window/app icon
        send start event
        manage event loop
        """
        queue = pygame2.core.platform.get_platform_event_queue()
        queue.start()

        window.bind('on_close', self.stop)

        self.running = True
        while self.running:
            self.clock.tick()

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
