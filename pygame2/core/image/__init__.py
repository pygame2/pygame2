from pygame2.core import core_modules

# declare our image providers
# core_modules['image'] = ('image_pil', 'image_pyglet', 'image_pygame')
core_modules['image'] = ('image_pil', 'image_pyglet')


class ImageLoaderBase:
    @staticmethod
    def load(filename, namehint=None):
        """
        load(filename) -> Surface
        load(fileobj, namehint='') -> Surface
        Load an image from a file source. You can pass either a filename or a
        Python file-like object.

        You should use os.path.join() for compatibility.
        """
        raise NotImplementedError

    @staticmethod
    def save(surface, filename):
        """Save an image to a file.

        :param surface: Surface to be saved
        :param filename: Filename to save to
        :return: None
        """
        raise NotImplementedError

    @staticmethod
    def get_extended():
        """Test if extended image formats can be loaded
        """
        raise NotImplementedError

    @staticmethod
    def tostring(surface, fmt, flipped=False):
        """Get surface image data in a string

        :param surface: pygame2.surface.Surface
        :param format: Image format to be returned
        :param flipped: Invert Y axis of image or not
        """
        raise NotImplementedError

    @staticmethod
    def fromstring(string, size, fmt, flipped=False):
        """Create new Surface from a string of data

        :param string: Surface to be saved
        :param size: Filename to save to
        :param format: Format of image data
        :param flipped: Invert Y axis of image or not
        :return: pygame2.surface.Surface
        """
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

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height


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
