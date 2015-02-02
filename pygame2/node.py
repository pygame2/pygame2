class Node:
    """GameTree Node
    """

    def __init__(self):
        self._children = set()
        self._order = list()

    def __contains__(self, item):
        return item in self._children

    def add(self, child):
        pass

    def remove(self, child):
        pass

    @property
    def children(self):
        pass


class SpriteNode(Node):
    """Essentially, anything drawable
    """
    pass
