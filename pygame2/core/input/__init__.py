"""
this module will define input devices not handled by
the window.  in practical terms this is most usb
devices including gamepads, joysticks, etc
"""
from pygame2.core import core_modules

# declare our platform providers
# core_modules['platform'] = ('platform_pyglet', 'platform_pygame',
# 'platform_pysdl2')

core_modules['input'] = ('input_pyglet', )

