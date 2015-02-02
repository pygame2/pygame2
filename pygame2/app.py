"""pygame2 app

* contains event loop
* dispatches events
* reads input
* manages audio
* has clock/scheduler
* handles screen/window/display updating
"""
from pygame2.event import EventDispatcher


class App(EventDispatcher):
    def __init__(self):
        # self._name = name
        # self._title = title
        pass

    def run(self):
        """
        create window
        set window title
        set window/app icon
        send start event
        manage event loop
        """
        pass

    def stop(self):
        pass
