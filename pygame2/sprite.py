"""
proposed sprite features:

-x/y scaling
-rotation (x, y, z)
-anchor points
"""
from abc import ABCMeta, abstractclassmethod
from pygame2.event import EventDispatcher


class SpriteBase(EventDispatcher, metaclass=ABCMeta):
    pass
