"""
"""

import pygame2
import pyglet
import pyglet.window
from pyglet import gl

__all__ = ['PygameDisplay',
           'init',
           'get_window',
           'set_mode',
           'set_caption',
           'get_caption',
           'toggle_fullscreen',
           'update',
           'flip',
           'get_surface',
           'quit',
           'get_init']


class SingletonMetaClass(type):
    _instance = None
    def __call__(cls, *args, **kw):
        if not cls._instance:
             cls._instance = super(SingletonMetaClass, cls).__call__(*args, **kw)
        return cls._instance


class PygameDisplay(metaclass=SingletonMetaClass):

    def __init__(self, resolution, flags=0, depth=0):
        if not hasattr(self, "_initialized"):
            w, h = resolution
            self._initialized = True
            self.resolution = resolution
            self.flags = flags
            self.depth = depth
            self.window = pyglet.window.Window(w, h)
            self.is_fullscreen = False
            self.blit_queue = list()

    def get_size(self):
        return self.resolution

    def get_height(self):
        return self.resolution[1]

    def get_width(self):
        return self.resolution[0]

    def get_rect(self):
        return pygame2.Rect((0, 0), self.resolution)

    def blit(self, source, dest, area=None, flags=0):
        self.blit_queue.append((source, dest, area, flags))

    def fill(self, color):
        """
        This currently will clear the entire window
        :param color:
        :return:
        """
        if len(color) == 3:
            color = list(color)
            color.append(1)

        # normalize the color, should be moved to a function/class sometime
        color = [float(i) / 255 for i in color]
        gl.glClearColor(*color)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)


def init():
    return None


def get_window():
    return PygameDisplay._instance.window


def set_mode(resolution, flags=0, depth=0):
    retval = PygameDisplay(resolution, flags, depth)
    print(PygameDisplay._instance)
    pygame2.key.init()
    return retval


def set_caption(title, icontitle=""):
    PygameDisplay._instance.window.set_caption(title)


def get_caption():
    return PygameDisplay._instance.window.caption


def toggle_fullscreen():
    instance = PygameDisplay._instance
    instance.is_fullscreen = not instance.is_fullscreen
    instance.window.set_fullscreen(instance.is_fullscreen)


def update(*args, **kwargs):
    flip()
    return None


def flip():
    instance = PygameDisplay._instance
    instance.window.switch_to()
    # instance.window.clear()
    for source, dest, area, flags in instance.blit_queue:
        x, y = dest[:2]
        source.get_imagedata().blit(x, y)
    instance.blit_queue = list()
    instance.window.flip()
    instance.window.invalid = False
    return None


def get_surface():
    return PygameDisplay._instance


def quit():
    PygameDisplay._instance = None
    return PygameDisplay._instance


def get_init():
    return PygameDisplay._instance is not None


# def quit():
# raise NotImplementedError()


# def set_mode(resolution=(0, 0), flags=0, depth=0):
#     raise NotImplementedError()


# def get_surface():
#     raise NotImplementedError()


# def flip():
#     raise NotImplementedError()


# def update(rectangle=None):
#     raise NotImplementedError()


# def get_driver():
#     raise NotImplementedError()


# def Info():
#     raise NotImplementedError()


# def get_wm_info():
#     raise NotImplementedError()


# def list_modes(depth, flags):
#     raise NotImplementedError()


# def mode_ok(size, flags=0, depth=None):
#     raise NotImplementedError()


# def gl_get_attribute(flag):
#     raise NotImplementedError()


# def gl_set_attribute(flag, value):
#     raise NotImplementedError()


# def get_active():
#     raise NotImplementedError()


# def iconify():
#     raise NotImplementedError()


# def toggle_fullscreen():
#     raise NotImplementedError()


# def set_gamma(red, green=None, blue=None):
#     raise NotImplementedError()


# def set_gamma_ramp(r, g, b):
#     raise NotImplementedError()


# def set_icon(icon):
#     raise NotImplementedError()


# def set_caption(title, icontitle=None):
#     raise NotImplementedError()


# def set_palette(palette=None):
#     raise NotImplementedError()
