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


class App(EventDispatcher):
    def __init__(self):
        # self._name = name
        # self._title = title
        self.clock = pygame2.clock.Clock()

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

        # event_loop = pygame2.core.platform.get_event_loop()

        while 1:
            queue.get()
            self.clock.tick()

            window.switch_to()
            # TODO: should dispatch event, not be called directly
            # window.dispatch_event('on_draw')
            window.on_draw()
            window.flip()

            sleep_time = self.clock.get_idle_time()
            # TODO: make sure we can sleep correctly on all systems
            # hack for now
            time.sleep(.005)


    def stop(self):
        pass
