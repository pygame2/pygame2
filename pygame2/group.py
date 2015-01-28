class SpriteGroup:
    """ AKA "renderer"
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
        """Return new list containing members of this group.

        :return: List
        """
        return list(self._members)

    def extend(self, sequence):
        """Add many sprites

        :param sequence: Sequence of Sprites
        :return: None
        """
        pass

    def add(self, sprite):
        """Add one sprite to the group

        :param sprite: Sprite
        :return: None
        """
        if sprite not in self._members:
            self.add_internal(sprite)
            sprite.add_internal(self)

    def remove(self, sprite):
        """Remove one sprite from the group

        :param sprite: Sprite
        :return: None
        """
        if sprite in self._members:
            self.remove_internal(sprite)
            sprite.remove_internal(self)

    def clear(self):
        """Remove all sprites from the group

        :return: None
        """
        for sprite in list(self._members):
            sprite.remove_internal(self)
            self.remove_internal(sprite)

    def draw(self):
        """draw all sprites that below to this group to the window"""
        pass
