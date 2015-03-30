"""
Image loading from pyglet.


USE PILLOW


Pyglet has many pure-python based image loading functions,
but tends to be slower than pygame or Pillow
"""

import pyglet

from . import ImageLoaderBase, ImageData


__all__ = ('ImageLoader', )


class ImageLoader(ImageLoaderBase):
    @staticmethod
    def load(filename, namehint=None):
        raise NotImplementedError

        if namehint is None:
            im = pyglet.image.load(filename)
        else:
            im = pyglet.image.load(namehint, file=filename)

        return ImageData(im.width, im.height, im.format, im.get_image_data())

    @staticmethod
    def save(surface, filename):
        # with open(filename, 'wb') as fh:
        # surface.get_imagedata().save(filename=filename, file=fh)
        raise NotImplementedError

    @staticmethod
    def get_extended():
        raise NotImplementedError

    @staticmethod
    def tostring(surface, format, flipped=False):
        # im = surface.get_imagedata()
        # pitch = -im.pitch if flipped else im.pitch
        # data = im.get_data(format, pitch)
        # return data
        raise NotImplementedError

    @staticmethod
    def fromstring(string, size, format, flipped=False):
        # pitch = size[0] * len(string)
        # if flipped:
        # pitch = -pitch
        # im = pyglet.image.ImageData(size[0], size[1], format, string, pitch)
        # return pygame2.surface.Surface.from_imagedata(im)
        raise NotImplementedError

    @staticmethod
    def frombuffer(string, size, format):
        raise NotImplementedError

    def tobuffer(surface, size, fmt, flipped=False):
        raise NotImplementedError
