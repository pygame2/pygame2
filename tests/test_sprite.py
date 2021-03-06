"""
all tests are borked until the opengl issues are sorted out
"""

import unittest
from unittest import skip
from mock import Mock, patch

from pygame2 import sprite, renderer
import OpenGL


class SpriteTests(unittest.TestCase):
    @skip("draw api not ready")
    def test_add_group(self):
        s = sprite.Sprite()
        g = renderer.SpriteRenderer()
        g.add(s)
        self.assertIn(s, g)

    @skip("draw api not ready")
    def test_remove_group(self):
        s = sprite.Sprite()
        g = renderer.SpriteRenderer()
        g.add(s)
        g.remove(s)
        self.assertNotIn(s, g)

    @skip("draw api not ready")
    def test_kill_removes_from_groups(self):
        g0 = renderer.SpriteRenderer()
        g1 = renderer.SpriteRenderer()
        s = sprite.Sprite()
        g0.add(s)
        g1.add(s)
        s.kill()
        self.assertNotIn(s, g0)
        self.assertNotIn(s, g1)


class GroupTests(unittest.TestCase):
    @skip("draw api not ready")
    def setUp(self):
        program = Mock()
        texture = Mock()
        self.g = renderer.SpriteRenderer(program, texture)

    @skip("draw api not ready")
    def test_sprites(self):
        self.assertEqual(len(self.g.sprites()), 0)

    # def test_copy(self):
    # self.fail()

    @skip("draw api not ready")
    def test_add(self):
        s = Mock()
        self.g.add(s)
        self.assertEqual(len(self.g.sprites()), 1)

    @skip("TODO: make a good exception for this error 'SpriteNotInGroup'?")
    def test_remove_raises(self):
        with self.assertRaises(KeyError):
            s = sprite.Sprite()
            self.g.remove(s)

    @skip("draw api not ready")
    def test_remove(self):
        s = sprite.Sprite()
        self.g.add(s)
        self.g.remove(s)
        self.assertEqual(len(self.g.sprites()), 0)

    @skip("draw api not ready")
    def test_has(self):
        s = sprite.Sprite()
        self.g.add(s)
        self.assertIn(s, self.g)

    @skip("draw api not ready")
    def test_update(self):
        s = Mock()
        self.g.add(s)

    @skip("draw api not ready")
    def test_draw(self):
        self.fail()

    @skip("draw api not ready")
    def test_clear(self):
        s0 = sprite.Sprite()
        self.g.add(s0)
        self.g.clear()
        self.assertEquals(len(self.g), 0)
