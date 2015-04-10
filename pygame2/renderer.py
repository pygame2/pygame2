"""
TODO: make some base class for the renderer
"""
from pygame2.group import SpriteGroupBase
from abc import ABCMeta, abstractclassmethod


class SpriteRendererBase(SpriteGroupBase, metaclass=ABCMeta):
    pass
