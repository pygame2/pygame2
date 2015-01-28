from pygame2.core import core_modules
# load our image providers

core_modules['image'] = ('image_pil', 'image_pyglet', 'image_pygame')


class ImageLoaderBase:

    @staticmethod
    def load(filename, namehint=None):
        raise NotImplementedError

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


class ImageData:
    """ Abstract Image as Bytes
    no mipmap support
    """
    _supported_fmts = ('rgb', 'rgba')

    def __init__(self, width, height, fmt, data, pitch=None, source=None):
        self._width = width
        self._height = height
        self._fmt = fmt.upper()
        self._data = data
        if not pitch:
            pitch = width * len(fmt)
        self._pitch = pitch
        self._source = source


def load(filename):
    """
    :param filename:Load an Image

    :return: ImageData instance
    """
    from pygame2.core import core_providers

    im = None
    for provider in core_providers['image']:
        try:
            im = provider.ImageLoader.load(filename)
            break
        except:
            raise

    return im
