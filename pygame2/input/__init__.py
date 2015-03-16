from pygame2.event import EventDispatcher

from . import gamepad
from . import keyboard
from . import mouse
from . import touch

__all__ = (
    'gamepad',
    'keyboard',
    'mouse',
    'touch',
    'Control',
    'RelativeAxis',
    'AbsoluteAxis',
    'Button')


class Control(EventDispatcher):
    """ Single value input provided by a device
    """
    def __init__(self, name):
        super().__init__()
        self.name = name
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not value == self._value:
            self._value = value
            self.dispatch('on_change')


class RelativeAxis(Control):
    pass


class AbsoluteAxis(Control):
    pass


class Button(Control):
    pass
