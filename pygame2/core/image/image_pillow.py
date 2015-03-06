"""
Image loading based on Pillow

Please do not use PIL
"""
from PIL import Image
from . import ImageLoaderBase, ImageData

__all__ = ('ImageLoader', )


class ImageLoader(ImageLoaderBase):
    @staticmethod
    def load(filename, namehint=None):
        """ Load an image

        This will open and decode an image and store the contents in memory.
        Currently, only RGBA mode images are supported as GPU Textures.

        :param filename:
        :param namehint:
        :return:
        """
        image = Image.open(filename)

        # Convert bitmap and palette images to component
        if image.mode in ('1', 'P'):
            image = image.convert()

        if image.mode not in ('L', 'LA', 'RGB',  'RGBA'):
            raise Exception('Unsupported mode "%s"' % image.mode)

        # TODO: make in-memory format configurable
        image = image.convert("RGBA")

        # tostring is deprecated, replaced by tobytes in Pillow (PIL fork)
        # (1.1.7) PIL still uses it
        image_xform = getattr(image, "tobytes", getattr(image, "tostring"))
        width, height = image.size

        return ImageData(width, height, image.mode,
                         image_xform('raw', 'RGBA', 0, -1))

    @staticmethod
    def save(surface, filename):
        raise NotImplementedError

    @staticmethod
    def get_extended():
        raise NotImplementedError

    @staticmethod
    def tostring(surface, fmt, flipped=False):
        raise NotImplementedError

    @staticmethod
    def fromstring(string, size, fmt, flipped=False):
        raise NotImplementedError

    @staticmethod
    def frombuffer(string, size, fmt, flipped=False):
        raise NotImplementedError

    @staticmethod
    def tobuffer(surface, size, fmt, flipped=False):
        raise NotImplementedError
