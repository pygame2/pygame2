from OpenGL.GL import *

mipmaps = 0

# TODO: MIPMAPS.  there is some code to support is, but isn't complete
# TODO: after mipmaps, implement texture streaming

"""
streaming texture overview:
    implement multiple opengl contexts
    implement context sharing between threads
    textures must use mipmaps
    all pygame2 textures (not data) are laoded at runtime
    when pygame2 textures are to be drawn, que message for loading thread
    render thread will use a dummy texture, or low resoultion mipmap (16x16?)
    loader thread will load texture, and make it available for draw thread
    draw thread will use the newly loaded texture
    occasionally, render thread will mark un used textures for destruction

why use streaming textures?
    everyone is doing it
    simplify state management
    easier for programmer/designer
    if done with threads, will provide stutter free texture use
    don't pause game while textures are loaded

why not:
    because it is complicated
    will require emulation of streaming textures
    streaming textures might be distracting
    doesn't work without shared context
    will not work on some hardware configurations

compromises:
    textures that are deemed too important for streaming have a flag attached
    render thread will watch queue
    if there are non-streamable textures, then pause main thread
    this is done assuming that game has 'loading screen'
        - mark GUI elements, player elements as important
        - mark background objects, particles, and clutter as not
        - game pauses while loading important things, then others will stream
        - best of both worlds
"""


class Texture:
    """ Textures

    pygame2 textures contain:
    - reference to a texture in opengl
    - code to upload texture data to gpu
    - code to set/unset opengl state for texturing primitives

    pygame2 textures do not store any texture data (that role is for Surfaces)
    textures only accept textures in this format: 32-bit RGBA, unsigned byte

    planned features
    - mipmaps
    - streaming
    - more formats
    """
    streamed = False
    target = GL_TEXTURE_2D

    def __init__(self, width, height, data):
        """Create new pygame2 texture

        :param width: width of image
        :param height: height of image
        :param data: bytes, image data
        :return:
        """
        self.id = None
        self.id = glGenTextures(1)

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
            GL_TEXTURE_2D, # target
            0, # level, 0 = no minimap
            GL_RGBA, # internalformat
            width, # width
            height, # height
            0, # border, always 0 in OpenGL ES
            GL_RGBA, # format
            GL_UNSIGNED_BYTE, # type
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

    def __del__(self):
        # id may not be set if binding/generation fails
        if self.id is not None:
            glDeleteTextures([self.id])

    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self.id)

    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)
