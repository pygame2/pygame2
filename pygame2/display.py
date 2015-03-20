"""
Abstract Hierarchy of Window Concepts:

'display', basically this is the gpu
'screen', could be the is a logical screen on one monitor or more
'window', as is
'canvas', drawing context for graphics.
"""


class Display:
    """ Display device containing one for more screens
    """
    def get_screens(self):
        """Get the available screens.

        A typical multi-monitor workstation comprises one :class:`Display`
        with multiple :class:`Screen` s.  This method returns a list of
        screens which can be enumerated to select one for full-screen display.

        For the purposes of creating an OpenGL config, the default screen
        will suffice.

        :rtype: list of :class:`Screen`
        """
        raise NotImplementedError('abstract')

    def get_default_screen(self):
        """Get the default screen as specified by the user's operating system
        preferences.

        :rtype: :class:`Screen`
        """
        return self.get_screens()[0]

    def get_windows(self):
        """Get the windows currently attached to this display.

        :rtype: sequence of :class:`~pygame2.window.Window`
        """
        raise NotImplementedError
