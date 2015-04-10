from collections import OrderedDict

from pygame2.event import EventDispatcher


__all__ = ('SpriteGroupBase', 'SpriteGroupSetList')


class AbstractGroup(EventDispatcher):
    """ AKA "renderer"
    """

    def __contains__(self, item):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def add_internal(self, member):
        raise NotImplementedError

    def remove_internal(self, member):
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

    def add(self, member):
        """Add one member to the group

        :param member: Member
        :return: None
        """
        raise NotImplementedError

    def remove(self, member):
        """Remove one member from the group

        :param member: Member
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


class OrderedGroup(AbstractGroup):
    """ Ordered container object optimized for speed and ease of use
    """

    def __init__(self):
        super().__init__()
        self._members = OrderedDict()

    def __contains__(self, item):
        return item in self._members

    def __len__(self):
        return len(self._members)

    def __iter__(self):
        return self._members.keys()

    def add_internal(self, member):
        self._members[member] = 0

    def remove_internal(self, member):
        del self._members[member]

    def sprites(self):
        return self._members.keys()

    def add(self, member):
        if member not in self._members:
            self.add_internal(member)
            member.add_internal(self)

    def extend(self, sequence):
        for member in sequence:
            if member not in self._members:
                self.add_internal(member)
                member.add_internal(self)

    def remove(self, member):
        if member in self._members.keys():
            self.remove_internal(member)
            member.remove_internal(self)

    def clear(self):
        for member in self._members.keys():
            member.remove_internal(self)
            self.remove_internal(member)

    def move_to_back(self, member):
        self._members.move_to_end(member, 1)

    def move_to_front(self, member):
        self._members.move_to_end(member, 0)


class GroupMember:
    """ class to be added to groups.  adds nice api for insertion and deletion
    """

    def __init__(self):
        self._groups = set()

    def add_internal(self, group):
        self._groups.add(group)

    def remove_internal(self, group):
        self._groups.remove(group)

    def kill(self):
        """remove the Member from all Groups
        Member.kill(): return None

        The Member is removed from all the Groups that contain it. This won't
        change anything about the state of the Member. It is possible to
        continue
        to use the Member after this method has been called, including adding it
        to Groups.
        """
        for g in list(self._groups):
            g.remove_internal(self)
        self._groups.clear()

    def groups(self):
        """list of Groups that contain this Member
        Member.groups(): return group_list

        Return a list of all the Groups that contain this Member.
        """
        return list(self._groups)
