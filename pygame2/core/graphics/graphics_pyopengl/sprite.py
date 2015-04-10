"""
proposed sprite features:

-x/y scaling
-rotation (x, y, z)
-anchor points
"""
from math import cos, sin
from math import radians

import numpy
from OpenGL.GL import *

from pygame2.sprite import SpriteBase
from .vbo import VertexBufferObject


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


class Sprite(SpriteBase):
    def update_transform(self):
        """ update VBO when affected by transforms or rotations

        :return: None
        """
        # self.vao = VertexArrayObject()
        # self.vao.bind()
        self.vbo = new_quad_vbo(self.rect, self.rotation)
        # glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        # glEnableVertexAttribArray(0)
