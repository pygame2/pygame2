from pygame2.event import EventDispatcher


class Sprite(EventDispatcher):
    """simple base class for visible game objects
    pygame.sprite.Sprite(*groups): return Sprite

    The base class for visible game objects. Derived classes will want to
    override the Sprite.update() and assign a Sprite.image and
    Sprite.rect attributes.  The initializer can accept any number of
    Group instances to be added to.

    When subclassing the Sprite, be sure to call the base initializer before
    adding the Sprite to Groups.
    """

    def __init__(self, *groups):
        self._groups = set()

    def add_internal(self, group):
        self._groups.add(group)

    def remove_internal(self, group):
        self._groups.remove(group)

    def update(self, *args):
        """method to control sprite behavior
        Sprite.update(*args):

        The default implementation of this method does nothing; it's just a
        convenient "hook" that you can override. This method is called by
        Group.update() with whatever arguments you give it.

        There is no need to use this method if not using the convenience
        method by the same name in the Group class.
        """
        pass

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
