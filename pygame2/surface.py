import pyglet
from pygame2.rect import Rect
from pyglet.image import ImageData, SolidColorImagePattern
from threading import Lock


__all__ = ['SubSurfaceData', 'Surface']


class SubSurfaceData:
    pass


class Surface:
    def __init__(self, size, flags=0, depth=0, masks=None):
        w, h = (int(i) for i in size)
        self._width = w
        self._height = h
        self._imagedata = pyglet.image.create(w, h)
        self._lock = Lock()

    def upload_to_gpu(self):
        pass

    @classmethod
    def from_imagedata(cls, imagedata):
        s = Surface((imagedata.width, imagedata.height))
        s._imagedata = imagedata
        return s

    def get_imagedata(self):
        return self._imagedata

    def get_lock(self):
        return self._lock

    def lock(self):
        self._lock.acquire()

    def unlock(self):
        self._lock.release()

    def fill(self, color, rect=None, special_flags=0):
        with self._lock:
            # TODO: this needs to be replaced with a proper color class
            if len(color) == 3:
                color = color[0], color[1], color[2], 0
            if rect is None:
                patt = SolidColorImagePattern(color)
                self._imagedata = patt.create_image(self._width, self._height)
            else:
                raise NotImplementedError

    def get_rect(self, **kwargs):
        return Rect(0, 0, self._width, self._height)

    def get_size(self):
        return self._imagedata.width, self._imagedata.height

    def get_width(self):
        return self._imagedata.width

    def get_height(self):
        return self._imagedata.height

    def get_region(self, area):
        """
        Get a region of the Surface's ImageData

        :param area: pygame2.Rect
        :rtype: pyglet.ImageDataRegion
        """
        return self._imagedata.get_region(*area)

