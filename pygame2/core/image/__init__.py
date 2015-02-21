from pygame2.core import core_modules
from OpenGL.GL import *

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

    def convert(self):
        return self._data.get_data('RGBA', self._data.pitch)

    def create_texture(self):
        """Create a texture containing this image.
        """
        pass
        # internalformat = self._get_internalformat(self.format)
        #
        # texture = cls.create(self.width, self.height, internalformat,
        # rectangle, force_rectangle)
        #
        # if self.anchor_x or self.anchor_y:
        #     texture.anchor_x = self.anchor_x
        #     texture.anchor_y = self.anchor_y
        #
        # self.blit_to_texture(texture.target, texture.level,
        #                      self.anchor_x, self.anchor_y, 0, None)
        # return texture

    def blit_to_texture(self, target, level, x, y, z, internalformat=None):
        """Draw this image to to the currently bound texture at `target`.

        This image's anchor point will be aligned to the given `x` and `y`
        coordinates.  If the currently bound texture is a 3D texture, the `z`
        parameter gives the image slice to blit into.

        If `internalformat` is specified, glTexImage is used to initialise
        the texture; otherwise, glTexSubImage is used to update a region.
        """
        pass
        # x -= self.anchor_x
        # y -= self.anchor_y
        #
        # data_format = self.format
        # data_pitch = abs(self._current_pitch)
        #
        # # Determine pixel format from format string
        # matrix = None
        # format, type = self._get_gl_format_and_type(data_format)
        # if format is None:
        # if (len(data_format) in (3, 4) and
        #             gl_info.have_extension('GL_ARB_imaging')):
        #         # Construct a color matrix to convert to GL_RGBA
        #         def component_column(component):
        #             try:
        #                 pos = 'RGBA'.index(component)
        #                 return [0] * pos + [1] + [0] * (3 - pos)
        #             except ValueError:
        #                 return [0, 0, 0, 0]
        #         # pad to avoid index exceptions
        #         lookup_format = data_format + 'TODO:'
        #         matrix = (component_column(lookup_format[0]) +
        #                   component_column(lookup_format[1]) +
        #                   component_column(lookup_format[2]) +
        #                   component_column(lookup_format[3]))
        #         format = {
        #             3: GL_RGB,
        #             4: GL_RGBA}.get(len(data_format))
        #         type = GL_UNSIGNED_BYTE
        #
        #         glMatrixMode(GL_COLOR)
        #         glPushMatrix()
        #         glLoadMatrixf((GLfloat * 16)(*matrix))
        #     else:
        #         # Need to convert data to a standard form
        #         data_format = {
        #             1: 'L',
        #             2: 'LA',
        #             3: 'RGB',
        #             4: 'RGBA'}.get(len(data_format))
        #         format, type = self._get_gl_format_and_type(data_format)
        #
        # # Workaround: don't use GL_UNPACK_ROW_LENGTH
        # if gl.current_context._workaround_unpack_row_length:
        #     data_pitch = self.width * len(data_format)
        #
        # # Get data in required format (hopefully will be the same format it's
        # # already in, unless that's an obscure format, upside-down or the
        # # driver is old).
        # data = self._convert(data_format, data_pitch)
        #
        # if data_pitch & 0x1:
        #     alignment = 1
        # elif data_pitch & 0x2:
        #     alignment = 2
        # else:
        #     alignment = 4
        # row_length = data_pitch // len(data_format)
        # glPushClientAttrib(GL_CLIENT_PIXEL_STORE_BIT)
        # glPixelStorei(GL_UNPACK_ALIGNMENT, alignment)
        # glPixelStorei(GL_UNPACK_ROW_LENGTH, row_length)
        # self._apply_region_unpack()
        #
        # if target == GL_TEXTURE_3D:
        #     assert not internalformat
        #     glTexSubImage3D(target, level,
        #                     x, y, z,
        #                     self.width, self.height, 1,
        #                     format, type,
        #                     data)
        # elif internalformat:
        #     glTexImage2D(target, level,
        #                  internalformat,
        #                  self.width, self.height,
        #                  0,
        #                  format, type,
        #                  data)
        # else:
        #     glTexSubImage2D(target, level,
        #                     x, y,
        #                     self.width, self.height,
        #                     format, type,
        #                     data)
        # glPopClientAttrib()
        #
        # if matrix:
        #     glPopMatrix()
        #     glMatrixMode(GL_MODELVIEW)
        #
        # # Flush image upload before data get GC'd.
        # glFlush()


def load(filename):
    """
    :param filename:Load an Image

    :return: Surface instance
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
