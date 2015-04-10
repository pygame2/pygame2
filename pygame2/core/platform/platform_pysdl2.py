"""
PySDL2 based platform
"""
from pygame2.event import PlatformEventQueueBase
from pygame2.window import WindowBase

# inform pysdl2 to look for the shared lib in the folder
# where this platform plugin is located
import os

os.environ['PYSDL2_DLL_PATH'] = os.path.dirname(__file__)

import sdl2
from sdl2 import video
import sdl2.ext

__all__ = ('PlatformEventQueue', 'Window')


class PlatformEventQueue(PlatformEventQueueBase):
    """ pysdl2 based event queue
    """

    def exit_blocking(self):
        pass

    def _blocking_timer(self):
        pass

    def enter_blocking(self):
        pass

    def start(self):
        sdl2.ext.init()

    def get(self, event_filter=None):
        return sdl2.ext.get_events()

    def post(self, event):
        pass

    def stop(self):
        pass

    def poll(self):
        pass

    def clear(self, event_filter=None):
        pass

    def peek(self, types=None):
        pass


class Window(WindowBase):
    __events__ = ('on_draw', 'on_close')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # set some defaults
        width, height = kwargs.get('size', (0, 0))
        kw = {
            'width': width,
            'height': height,
            'caption': self._caption,
            'resizable': self._resizable,
            'fullscreen': self._fullscreen,
            'visible': self._visible,
            'vsync': self._vsync,
        }

        window = sdl2.SDL_CreateWindow(b"OpenGL demo",
                                       sdl2.SDL_WINDOWPOS_UNDEFINED,
                                       sdl2.SDL_WINDOWPOS_UNDEFINED, 800, 600,
                                       sdl2.SDL_WINDOW_OPENGL)


        # set opengl context to 3.3, our defined minimum
        # must be done before creating the context
        video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
        video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MINOR_VERSION, 3)
        video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_PROFILE_MASK,
                                  video.SDL_GL_CONTEXT_PROFILE_CORE)

        # Double buffering is on
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER, 1)

        context = sdl2.SDL_GL_CreateContext(window)

        # vsync is on
        sdl2.SDL_GL_SetSwapInterval(1)

        self._window = window
        self._context = context

    def activate(self):
        pass

    def flip(self):
        sdl2.SDL_GL_SwapWindow(self._window)

    def switch_to(self):
        sdl2.SDL_GL_MakeCurrent(self._window, self._context)

    def dispatch_pending_events(self):
        pass

    def close(self):
        sdl2.SDL_GL_DeleteContext(self._context)
        # sdl2.SDL_DestroyWindow(window)
        self._window = None

    def minimize(self):
        pass

    def maximize(self):
        pass

