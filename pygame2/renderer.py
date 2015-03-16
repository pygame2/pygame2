"""
As is, this sprite/group implementation will only
work with the pyglet backend
"""
from collections import OrderedDict
from pygame2.event import EventDispatcher
from pygame2.graphics import *
from OpenGL.GL import *

__all__ = (
    'SpriteGroupBase',
    'SpriteGroupSetList',
    'SpriteGroup')


class SpriteGroupBase(EventDispatcher):
    """ AKA "renderer"
    """

    def __contains__(self, item):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def add_internal(self, sprite):
        raise NotImplementedError

    def remove_internal(self, sprite):
        raise NotImplementedError

    def sprites(self):
        """Return new list containing members of this group.

        :return: List
        """
        raise NotImplementedError

    def extend(self, sequence):
        """Add many sprites

        :param sequence: Sequence of Sprites
        :return: None
        """
        raise NotImplementedError

    def add(self, sprite):
        """Add one sprite to the group

        :param sprite: Sprite
        :return: None
        """
        raise NotImplementedError

    def remove(self, sprite):
        """Remove one sprite from the group

        :param sprite: Sprite
        :return: None
        """
        raise NotImplementedError

    def clear(self):
        """Remove all sprites from the group

        :return: None
        """
        raise NotImplementedError

    def draw(self):
        """draw all sprites that below to this group to the window"""
        pass


class SpriteGroupSetList(SpriteGroupBase):
    """ Mix list and set

    AKA "renderer"
    """

    def __init__(self):
        super().__init__()
        self._members = set()
        self._order = list()

    def __contains__(self, item):
        return item in self._members

    def __len__(self):
        return len(self._members)

    def __iter__(self):
        return list(self._order)

    def add_internal(self, sprite):
        self._members.add(sprite)
        self._order.append(sprite)

    def remove_internal(self, sprite):
        self._members.remove(sprite)
        self._order.remove(sprite)

    def sprites(self):
        return list(self._members)

    def add(self, sprite):
        if sprite not in self._members:
            self.add_internal(sprite)
            sprite.add_internal(self)

    def remove(self, sprite):
        if sprite in self._members:
            self.remove_internal(sprite)
            sprite.remove_internal(self)

    def clear(self):
        for sprite in list(self._members):
            sprite.remove_internal(self)
            self.remove_internal(sprite)


class SpriteGroupBase(SpriteGroupBase):
    """OrderedDict
    """

    def __init__(self):
        super().__init__()
        self._members = OrderedDict()

    def __contains__(self, item):
        return item in self._members

    def __len__(self):
        return len(self._members)

    def __iter__(self):
        return self._members.keys()

    def add_internal(self, sprite):
        self._members[sprite] = 0

    def remove_internal(self, sprite):
        del self._members[sprite]

    def sprites(self):
        return self._members.keys()

    def extend(self, sequence):
        pass

    def add(self, sprite):
        if sprite not in self._members:
            self.add_internal(sprite)
            sprite.add_internal(self)

    def remove(self, sprite):
        if sprite in self._members:
            self.remove_internal(sprite)
            sprite.remove_internal(self)

    def clear(self):
        for sprite in self._members.keys():
            sprite.remove_internal(self)
            self.remove_internal(sprite)


class SpriteRenderer(SpriteGroupBase):
    """ A group that contains sprites with identical OpenGL state.

    Sprites with the same state will be drawn together
    for better performance.
    """
    mode = GL_TRIANGLE_STRIP

    def __init__(self, program):
        super().__init__()
        self.program = program

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

            # bind the vbo and render the group's texture to these coords
            sprite.vbo.bind()
            glVertexAttribPointer(attr, 2, GL_FLOAT, GL_FALSE, 0, None)

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
