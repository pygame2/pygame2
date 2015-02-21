from . import ImageLoaderBase, ImageData
# import pygame
import os


class ImageLoader(ImageLoaderBase):
    """ fairly useless as it requires the
    pygame display to be initialized
    """

    @staticmethod
    def load(filename, namehint=None):
        # fn, ext = os.path.splitext(filename)
        # im = pygame.image.load(filename, ext)
        #
        # fmt = ''
        # if im.get_bytesize() == 3:
        # fmt = 'rgb'
        # elif im.get_bytesize() == 4:
        #     fmt = 'rgba'
        # else:
        #     im = im.convert(32)
        #     fmt = 'rgba'
        # data = pygame.image.tostring(im, fmt.upper())
        # return ImageData(im.get_width(), im.get_height(), fmt, data,
        #                  source=filename)
        raise Exception

    @staticmethod
    def save(surface, filename):
        raise NotImplementedError

    @staticmethod
    def get_extended():
        raise NotImplementedError

    @staticmethod
    def tostring(surface, format, flipped=False):
        raise NotImplementedError

    @staticmethod
    def fromstring(string, size, format, flipped=False):
        raise NotImplementedError

    @staticmethod
    def frombuffer(string, size, format, flipped=False):
        raise NotImplementedError

    @staticmethod
    def tobuffer(surface, size, format, flipped=False):
        raise NotImplementedError
