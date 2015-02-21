"""
Application windows and input events are closely tied together,
so they have been lumped together in a generic 'platform'
interface.  A platform consists of the following:
  Window or windows
  Event Loop
  Input Interfaces

Where possible, if a platform provides functions that do not depend
on the functions listed above, then that functionality will be
split up and made into a separate module.
"""
from pygame2.core import core_modules

# declare our image providers
# core_modules['platform'] = ('platform_pyglet', 'platform_pygame',
#                             'platform_pysdl2')

core_modules['platform'] = ('platform_pyglet', )


def get_event_loop():
    pass


def get_platform_event_queue():
    """
    :return: Pygame2 event queue (depends on platform)
    """
    from pygame2.core import core_providers

    queue = None
    for provider in core_providers['platform']:
        try:
            queue = provider.PlatformEventQueue()
            break
        except:
            raise

    return queue


def create_window(**kwargs):
    """
    :return: Pygame2 window (depends on event queue)
    """
    from pygame2.core import core_providers

    win = None
    for provider in core_providers['platform']:
        try:
            win = provider.Window(**kwargs)
            break
        except:
            raise

    return win
