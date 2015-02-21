"""
As is, this sprite/group implementation will only
work with the pyglet backend
"""
from collections import OrderedDict
from pygame2.event import EventDispatcher
from OpenGL.GL import *


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


class RenderGroup(SpriteGroupBase):
    """ A group that contains sprites with identical OpenGL state.

    Sprites with the same state will be drawn together
    for better performance.
    """
    pass


class Batch:
    """Manage a collection of vertex lists for batched rendering.

    Vertex lists are added to a `Batch` using the `add` and `add_indexed`
    methods.  An optional group can be specified along with the vertex list,
    which gives the OpenGL state required for its rendering.  Vertex lists
    with shared mode and group are allocated into adjacent areas of memory and
    sent to the graphics card in a single operation.

    Call `VertexList.delete` to remove a vertex list from the batch.
    """
    def __init__(self, program):
        self.program = program
        self.mode = GL_TRIANGLE_STRIP

        self.attr = dict()
        for name in 'coord2d texcoord'.split():
            self.attr[name] = self.bind_attribute(name)

        # hack
        # either the batch or program should be maintaining
        # vertex array attributes.  it lives here as a test
        self._attr = dict()
        attr_texcoord = self.attr['texcoord']
        attr_coord2d = self.attr['coord2d']
        self._attr[attr_texcoord] = None
        self._attr[attr_coord2d] = None

    def bind_attribute(self, name):
        """bind attribute name and return value
        """
        attr = glGetAttribLocation(self.program, name)
        assert (not attr == -1)
        return attr

    def draw(self):
        self.set_state()
        # TODO: get number of vertices to draw
        vertices = 4
        glDrawArrays(self.mode, 0, vertices)
        # glFlush()
        self.unset_state()

    def set_state(self):
        glUseProgram(self.program)

        # just hacks for now
        uniform_id = glGetUniformLocation(self.program, 'mytexture')
        glUniform1i(uniform_id, 0)

        # for attr, vbo in self._attr.items():
        #     glEnableVertexAttribArray(attr)
        #     vbo.bind()
        #     glVertexAttribPointer(attr, 3, GL_FLOAT, GL_FALSE, 0, None)

        attr = self.attr['coord2d']
        vbo = self._attr[attr]
        glEnableVertexAttribArray(attr)
        vbo.bind()
        glVertexAttribPointer(attr, 2, GL_FLOAT, GL_FALSE, 0, None)

        attr = self.attr['texcoord']
        vbo = self._attr[attr]
        glEnableVertexAttribArray(attr)
        vbo.bind()
        glVertexAttribPointer(attr, 2, GL_FLOAT, GL_FALSE, 0, None)

    def unset_state(self):
        for attrib in self.attr.values():
            glDisableVertexAttribArray(attrib)


class SpriteGroup(RenderGroup):
    """sprite groups share a common texture and state"""
    def __init__(self, program, texture):
        super().__init__()
        self.batch = Batch(program)
        self.program = program
        self.texture = texture

    def draw(self):
        self.set_state()
        self.batch.draw()
        self.unset_state()

    def set_state(self):
        target = self.texture.target
        glEnable(target)
        glTexParameterf(target, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        #glTexParameterf(target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        #glTexParameteri(target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glDepthMask(0)  # disable writing to depth buffer
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_COLOR, GL_ONE_MINUS_SRC_ALPHA)

        glActiveTexture(GL_TEXTURE0)
        self.texture.bind()

    def unset_state(self):
        glDisable(self.texture.target)
        glDisable(GL_BLEND)
        glDepthMask(1)
