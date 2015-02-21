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
        image = Image.open(filename)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)

        # Convert bitmap and palette images to component
        if image.mode in ('1', 'P'):
            image = image.convert()

        if image.mode not in ('L', 'LA', 'RGB', 'RGBA'):
            raise Exception('Unsupported mode "%s"' % image.mode)

        # tostring is deprecated, replaced by tobytes in Pillow (PIL fork)
        # (1.1.7) PIL still uses it
        image_data_fn = getattr(image, "tobytes", getattr(image, "tostring"))
        width, height = image.size
        return ImageData(width, height, image.mode, image_data_fn())

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
