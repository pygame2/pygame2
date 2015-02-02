"""
As is, this sprite/group implementation will only
work with the pyglet backend
"""
from collections import OrderedDict
from pygame2.event import EventDispatcher


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
    """
    As is, this sprite/group implementation will only
    work with the pyglet backend
    """
    pass


class SpriteGroup(RenderGroup):
    pass
