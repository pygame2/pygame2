import unittest
from unittest import skip
from mock import Mock, MagicMock

from pygame2 import sprite, group


class SpriteTests(unittest.TestCase):
    def test_add_group(self):
        s = sprite.Sprite()
        g = group.SpriteGroup()
        g.add(s)
        self.assertIn(s, g)

    def test_remove_group(self):
        s = sprite.Sprite()
        g = group.SpriteGroup()
        g.add(s)
        g.remove(s)
        self.assertNotIn(s, g)

    def test_kill_removes_from_groups(self):
        g0 = group.SpriteGroup()
        g1 = group.SpriteGroup()
        s = sprite.Sprite()
        g0.add(s)
        g1.add(s)
        s.kill()
        self.assertNotIn(s, g0)
        self.assertNotIn(s, g1)


class GroupTests(unittest.TestCase):
    def setUp(self):
        self.g = group.SpriteGroup()

    def test_sprites(self):
        self.assertEqual(len(self.g.sprites()), 0)

    # def test_copy(self):
    # self.fail()

    def test_add(self):
        s = Mock()
        self.g.add(s)
        self.assertEqual(len(self.g.sprites()), 1)

    @skip("TODO: make a good exception for this error 'SpriteNotInGroup'?")
    def test_remove_raises(self):
        with self.assertRaises(KeyError):
            s = sprite.Sprite()
            self.g.remove(s)

    def test_remove(self):
        s = sprite.Sprite()
        self.g.add(s)
        self.g.remove(s)
        self.assertEqual(len(self.g.sprites()), 0)

    def test_has(self):
        s = sprite.Sprite()
        self.g.add(s)
        self.assertIn(s, self.g)

    def test_update(self):
        s = Mock()
        self.g.add(s)

    @skip("draw api not ready")
    def test_draw(self):
        self.fail()

    def test_clear(self):
        g = group.SpriteGroup()
        s0 = sprite.Sprite()
        g.add(s0)
        g.clear()
        self.assertEquals(len(g), 0)
