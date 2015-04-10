"""
Mostly, it will be the graphics backend that implements rendering
"""
from pygame2.group import OrderedGroup
from abc import ABCMeta, abstractclassmethod


class SpriteRendererBase(OrderedGroup, metaclass=ABCMeta):

    @abstractclassmethod
    def draw(self):
        raise NotImplementedError
