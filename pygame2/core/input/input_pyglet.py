""" pyglet keyboard and mouse interface

JUST A STUB - REAL HANDLING IS DONE BY THE WINDOW

pyglet is almost a pure event oriented framework, so the way pygame2
handles it will seem awkward:
   - set event handlers for each input
   - catch events and queue them

if we are to remove this queue/dequeue steps, then we'll have to
fork pyglet and use pyglet's excellet ctypes-based OS interfaces and
then handle the queue directly.
"""
from pygame2.input.keyboard import KeyboardBase
from pygame2.input.mouse import MouseBase


class Keyboard(KeyboardBase):
    pass


class Mouse(MouseBase):
    pass
