"""
pygame2 image abstractions

ImageData => data that represents image in variety of formats
             able to be converted into other formats
Surface   => contains ImageData, able to be 'drawn' onto screen
             will include some warnings if manually manipulated
Sprite    => contains Texture, able to be manipulated easily
             able to live in groups and batches
Animation => contains Several surfaces, operated like Sprite

future:
As images are loaded from disk, they will be converted to a
common pixel format, and grouped into large textures.

It will be up to the programmer to give pygame2 hints which
images should be shared on a texture, and it will give a
performance penalty if commonly-used-together textures are
often not drawn together.
"""

from pygame2.rect import Rect
from threading import Lock


__all__ = ('SubSurfaceData', 'Surface')


class SubSurfaceData:
    pass


class Surface:
    def __init__(self, size, flags=0, depth=0, masks=None):
        w, h = (int(i) for i in size)
        self._width = w
        self._height = h
        self._imagedata = None
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
        pass

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

