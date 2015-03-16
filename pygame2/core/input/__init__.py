"""
this module will define input devices not handled by
the window.  in practical terms this is most usb
devices including gamepads, joysticks, etc

keyboard and mouse events will most likely come from
the core platform, but that is not guaranteed across
platforms.
"""
from pygame2.core import core_modules

core_modules['input'] = ('input_pyglet', )


def get_keyboard(**kwargs):
    """
    :return: Pygame2 window (depends on event queue)
    """
    from pygame2.core import core_providers

    keyboard = None
    for provider in core_providers['input']:
        try:
            keyboard = provider.Keyboard(**kwargs)
            break
        except:
            raise

    return keyboard