"""
Abstract Hierarchy of Window Concepts:

'display', basically this is the gpu
'screen', could be the is a logical screen on one monitor or more
'window', as is
'canvas', drawing context for graphics.
"""


class Screen:
    """A virtual monitor that supports fullscreen windows.

    Screens typically map onto a physical display such as a
    monitor, television or projector.  Selecting a screen for a window
    has no effect unless the window is made fullscreen, in which case
    the window will fill only that particular virtual screen.

    The :attr:`width` and :attr:`height` attributes of a screen give the
    current resolution of the screen.  The :attr:`x` and :attr:`y` attributes
    give the global location of the top-left corner of the screen.  This is
    useful for determining if screens arranged above or next to one another.

    Use :func:`~Display.get_screens` or :func:`~Display.get_default_screen`
    to obtain an instance of this class.

    :guide:`screens`
    """
    def __init__(self):
        pass

    def create_window(self, *args, **kwargs):
        raise NotImplementedError
