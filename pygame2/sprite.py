"""
proposed sprite features:

-x/y scaling
-rotation (x, y, z)
-anchor points
"""
from math import cos, sin
from math import radians
import numpy

from pygame2.animation import Animated
from pygame2.event import EventDispatcher
from pygame2.graphics import *
from pygame2.rect import Rect

from OpenGL.GL import *

__all__ = ('Sprite', )


def new_quad_vbo(rect, rotation=0):
    x, y, width, height = rect

    # TODO: get anchor of rect
    x1 = 0
    y1 = 0
    x2 = x1 + width
    y2 = y1 + height

    r = -radians(rotation)
    cr = cos(r)
    sr = sin(r)
    ax = x1 * cr - y1 * sr + x
    ay = x1 * sr + y1 * cr + y
    bx = x2 * cr - y1 * sr + x
    by = x2 * sr + y1 * cr + y
    dx = x2 * cr - y2 * sr + x
    dy = x2 * sr + y2 * cr + y
    cx = x1 * cr - y2 * sr + x
    cy = x1 * sr + y2 * cr + y

    vertices = numpy.array([ax, ay, bx, by, cx, cy, dx, dy], dtype='float32')
    vbo = VertexBufferObject(vertices, GL_ARRAY_BUFFER, GL_STATIC_DRAW)
    return vbo


class Sprite(EventDispatcher, Animated):
    """simple base class for visible game objects

    When subclassing the Sprite, be sure to call the base initializer before
    adding the Sprite to Groups.

    When making game objects (players, missiles, etc), it is advisable to
    follow the composite pattern, rather than subclassing this.

    One important concept to think about is that there are no
    "animated sprites".  Sprites can be thought of as simply
    'just enough' data to show a texture somewhere on the screen,
    and are not enough to be game objects.

    To make an abstraction of game objects whose graphical representation
    will change over time (animate), then sprites should be treated like
    individual frames of the animation.

    the exception to the above statement would be when each animation frame
    is the same size as the rest.  in this case, it would be acceptable
    to simply change the texture that the sprite refers to.
    """

    def __init__(self, texture=None):
        super().__init__()
        self._groups = set()
        self.rotation = 0
        self.scale = 1.0, 1.0  # unused for now
        self.shear = None      # unused for now
        self.vbo = None
        self.texture = texture

        # TODO: fix the rect stuff below
        self.rect = Rect(0, 0, 1, 1)
        self.update_transform()

    def add_internal(self, group):
        self._groups.add(group)

    def remove_internal(self, group):
        self._groups.remove(group)

    def update_transform(self):
        """ update VBO when affected by transforms or rotations
        :return: None
        """
        self.vbo = new_quad_vbo(self.rect, self.rotation)

    def kill(self):
        """remove the Sprite from all Groups
        Sprite.kill(): return None

        The Sprite is removed from all the Groups that contain it. This won't
        change anything about the state of the Sprite. It is possible to
        continue
        to use the Sprite after this method has been called, including adding it
        to Groups.
        """
        for g in list(self._groups):
            g.remove_internal(self)
        self._groups.clear()

    def groups(self):
        """list of Groups that contain this Sprite
        Sprite.groups(): return group_list

        Return a list of all the Groups that contain this Sprite.
        """
        return list(self._groups)

    def alive(self):
        """does the sprite belong to any groups
        Sprite.alive(): return bool

        Returns True when the Sprite belongs to one or more Groups.
        """
        return bool(self._groups)

    def __repr__(self):
        return "<%s sprite(in %d groups)>" % (
            self.__class__.__name__, len(self._groups))
