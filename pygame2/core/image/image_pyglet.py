import pygame2
import pyglet
from . import ImageLoaderBase, ImageData

__all__ = ['ImageLoaderPyglet']


class ImageLoader(ImageLoaderBase):

    @staticmethod
    def load(filename, namehint=None):
        """
        load(filename) -> Surface
        load(fileobj, namehint='') -> Surface
        Load an image from a file source. You can pass either a filename or a Python
        file-like object.

        Pygame will automatically determine the image type (e.g., GIF or bitmap) and
        create a new Surface object from the data. In some cases it will need to
        know the file extension (e.g., GIF images should end in '.gif'). If you pass
        a raw file-like object, you may also want to pass the original filename as
        the namehint argument.

        You should use os.path.join() for compatibility.
        """
        if namehint is None:
            im = pyglet.image.load(filename)
        else:
            im = pyglet.image.load(namehint, file=filename)

        return pygame2.surface.Surface.from_imagedata(im)

    @staticmethod
    def save(surface, filename):
        """Save an image to a file.

        This is just an API relic from pygame1, and just calls surface.save()

        :param surface: Surface to be saved
        :param filename: Filename to save to
        :return: None
        """
        with open(filename, 'wb') as fh:
            surface.get_imagedata().save(filename=filename, file=fh)

    @staticmethod
    def get_extended():
        """Test if extended image formats can be loaded

        If pygame is built with extended image formats this function will return
        True. It is still not possible to determine which formats will be available,
        but generally you will be able to load them all.
        """
        raise NotImplementedError

    @staticmethod
    def tostring(surface, format, flipped=False):
        """Get surface image data in a string

        :param surface: pygame2.surface.Surface
        :param format: Image format to be returned
        :param flipped: Invert Y axis of image or not
        """
        im = surface.get_imagedata()
        pitch = -im.pitch if flipped else im.pitch
        data = im.get_data(format, pitch)
        return data

    @staticmethod
    def fromstring(string, size, format, flipped=False):
        """Create new Surface from a string of data

        :param string: Surface to be saved
        :param size: Filename to save to
        :param format: Format of image data
        :param flipped: Invert Y axis of image or not
        :return: pygame2.surface.Surface
        """
        pitch = size[0] * len(string)
        if flipped:
            pitch = -pitch
        im = pyglet.image.ImageData(size[0], size[1], format, string, pitch)
        return pygame2.surface.Surface.from_imagedata(im)

    @staticmethod
    def frombuffer(string, size, format):
        raise NotImplementedError
