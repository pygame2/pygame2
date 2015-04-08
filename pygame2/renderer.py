"""
As is, this sprite/group implementation will only
work with the pyglet backend
"""
from pygame2.graphics import *
from pygame2.group import SpriteGroupBase
from pygame2.sprite import Sprite
from OpenGL.GL import *

__all__ = ('SpriteRenderer', )


class SpriteRenderer(SpriteGroupBase):
    """ A group that contains sprites with identical OpenGL state.

    Sprites with the same state will be drawn together
    for better performance.
    """
    mode = GL_TRIANGLE_STRIP
    shaders=[('vertex_shader.glsl', GL_VERTEX_SHADER),
             ('fragment_shader.glsl', GL_FRAGMENT_SHADER)]

    def __init__(self):
        super().__init__()
        self.program = create_program(self.shaders)

        self.attr = dict()
        for name in 'coord2d texcoord'.split():
            self.attr[name] = self.bind_attribute(name)

        # hack
        # either the batch or program should be maintaining
        # vertex array attributes.  it lives here as a test
        self._attr = dict()
        attr_texcoord = self.attr['texcoord']
        attr_coord2d = self.attr['coord2d']
        self._attr[attr_texcoord] = generate_tex_coords()
        self._attr[attr_coord2d] = None

    # def __del__(self):
    #     glDetachShader(self.program, vertexshader)
    #     glDetachShader(self.program, fragmentshader)
    #     glDeleteProgram(self.program)
    #     glDeleteShader(vertexshader)
    #     glDeleteShader(fragmentshader)
    #     glDeleteBuffers(2, vbo)
    #     glDeleteVertexArrays(1, &vao)

    def create_sprite(self, *args, **kwargs):
        sprite = Sprite(*args, **kwargs)
        self.add(sprite)
        return sprite

    def create_texture(self, surface):
        """Create a texture containing this image.
        """
        # TODO: textures made here since format is dependant on renderer
        width, height = surface.size
        return Texture(width, height, surface._data)

    def bind_attribute(self, name):
        """bind attribute name and return value
        """
        attr = glGetAttribLocation(self.program, name)
        assert (not attr == -1)
        return attr

    def draw(self):
        self.set_state()

        # start changing the coord2d in program
        attr = self.attr['coord2d']
        glEnableVertexAttribArray(attr)

        # assumes we are just rendering 4 vertex triangle strips
        for sprite in self.sprites():
            self.set_texture(sprite.texture)

            sprite.vbo.bind()

            # draw
            glDrawArrays(self.mode, 0, 4)

            self.unset_texture(sprite.texture)

        self.unset_state()

    def set_state(self):
        glUseProgram(self.program)
        uniform_id = glGetUniformLocation(self.program, 'mytexture')
        glUniform1i(uniform_id, 0)

        # for attr, vbo in self._attr.items():
        # glEnableVertexAttribArray(attr)
        # vbo.bind()
        #     glVertexAttribPointer(attr, 3, GL_FLOAT, GL_FALSE, 0, None)

        # set the texture coordinates
        attr = self.attr['texcoord']
        vbo = self._attr[attr]
        glEnableVertexAttribArray(attr)
        vbo.bind()
        glVertexAttribPointer(attr, 2, GL_FLOAT, GL_FALSE, 0, None)

    def set_texture(self, texture):
        target = texture.target
        glEnable(target)

        # linear filters, not sure if needed here, since it
        # is already set in the texture
        # glTexParameterf(target, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        # uncomment below for pixelated look
        # glTexParameterf(target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        # glTexParameteri(target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glActiveTexture(GL_TEXTURE0)
        texture.bind()

    def unset_texture(self, texture):
        glDisable(texture.target)

    def unset_state(self):
        glDisable(GL_BLEND)

        for attrib in self.attr.values():
            glDisableVertexAttribArray(attrib)

        glUseProgram(0)
        glBindVertexArray(0)