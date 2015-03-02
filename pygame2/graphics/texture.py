from OpenGL.GL import *

mipmaps = 0


def load_texture(flip_y=False):
    """ Texture loading with PIL

    :param flip_y:
    :return: pygame2.graphics.Texture
    """
    import os
    from PIL import Image

    path = os.path.join('resources', 'pygame2.png')


    image = Image.open(path)
    width, height = image.size
    image = image.convert("RGBA")
    if flip_y:
        image = image.transpose(Image.FLIP_TOP_BOTTOM)

    # BGRA pixel ordering is preferred on some platforms, possibly windows
    # other orderings will work, but will have a performance penalty as
    # data in automatically changed to the preferred ordering in the opengl API
    data = image.tostring('raw', 'RGBA', 0, -1)

    # pygame2 image loading
    # image = pygame2.core.image.load(path)
    # data = str(image.convert())
    # data = numpy.fromstring(data, dtype='uint8')

    texture = Texture(width, height, data)
    return texture


class Texture:
    def __init__(self, width, height, data):
        self.target = GL_TEXTURE_2D

        id = glGenTextures(1)
        self.id = id

        # TODO: check for NPOT limitations

        self.bind()

        if mipmaps:
            # required for automatic mipmaps on legacy ATI systems
            glEnable(GL_TEXTURE_2D)
        else:
            # required on some platforms to deal with images without mipmaps
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)

        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        # no texture storage api until 4.3
        glTexImage2D(
            GL_TEXTURE_2D,  # target
            0,  # level, 0 = no minimap
            GL_RGBA,  # internalformat
            width,  # width
            height,  # height
            0,  # border, always 0 in OpenGL ES
            GL_RGBA,  # format
            GL_UNSIGNED_BYTE,  # type
            data  # pixel data
        )

        if mipmaps:
            # generate mipmaps automatically
            glGenerateMipmap(GL_TEXTURE_2D)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                            GL_LINEAR_MIPMAP_LINEAR)

            # required for automatic mipmaps on legacy ATI systems
            glDisable(GL_TEXTURE_2D)

        self.unbind()

    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self.id)

    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)

    def __del__(self):
        self.delete()

    def delete(self):
        glDeleteTextures([self.id])
        self.id = None
