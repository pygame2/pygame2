"""
proposed sprite features:

-x/y scaling
-rotation (x, y, z)
-anchor points
"""
from abc import ABCMeta, abstractclassmethod

from pygame2.animation import Animated
from pygame2.event import EventDispatcher
from pygame2.group import GroupMember
from pygame2.rect import Rect


class SpriteBase(GroupMember, EventDispatcher, Animated, metaclass=ABCMeta):
    def __init__(self, texture=None):
        super().__init__()
        self.rotation = 0
        self.scale = 1.0, 1.0  # unused for now
        self.shear = None      # unused for now
        self.vbo = None
        self.vao = None
        self.texture = texture
        self.rect = Rect(0, 0, 1, 1)

        self.update_transform()

    @abstractclassmethod
    def update_transform(self):
        raise NotImplementedError

    def __repr__(self):
        return "<%s sprite(in %d groups)>" % (
            self.__class__.__name__, len(self._groups))
