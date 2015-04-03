"""
Surface Tests

"""

from unittest import TestCase, skip
from mock import MagicMock
from logging import getLogger

from pygame2.surface import Surface
from pygame2.rect import Rect

logger = getLogger()


class SurfaceTests(TestCase):
    def setUp(self):
        self.size = (32, 32)
        self.s = Surface(self.size)

    def test_fill(self):
        """ Just test and make sure no exceptions are raised
        """
        self.s.fill((0, 0, 0))
        self.s.fill((0, 0, 0, 0))

    def test_get_rect(self):
        rect = Rect((0, 0), self.size)
        self.assertEquals(rect, self.s.get_rect())

    @skip('needs refactor')
    def test_get_size(self):
        size = self.s.get_size()
        self.assertEquals(self.size, size)

    @skip('needs refactor')
    def test_get_width(self):
        width = self.s.get_width()
        self.assertEquals(self.size[0], width)

    @skip('needs refactor')
    def test_get_height(self):
        height = self.s.get_height()
        self.assertEquals(self.size[1], height)

    def test_lock(self):
        """ Just test and make sure no exceptions are raised
        """
        self.s.lock()
        self.s.unlock()

    def test_unlock(self):
        """ Just test and make sure no exceptions are raised
        """
        self.s.lock()
        self.s.unlock()

    def test_from_imagedata(self):
        """sets the size and image data member of the surface"""
        imagedata = MagicMock()
        imagedata.width = 10
        imagedata.height = 15
        s = self.s.from_imagedata(imagedata)
        self.assertEquals(s.get_rect().size, (10, 15))
        self.assertIs(imagedata, s.get_imagedata())

    def test_get_lock(self):
        self.assertIs(self.s._lock, self.s.get_lock())
