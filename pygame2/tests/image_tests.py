"""
Pygame.image Tests
"""

from unittest import TestCase
from logging import getLogger
import os

import pygame2


logger = getLogger()
supported_formats = ['P',
                     'RGB',
                     'RGBX',
                     'RGBA',
                     'ARGB',
                     'RGBA_PREMULT',
                     'ARGB_PREMULT']

default_generic_filename = 'pygame2'
default_filename = default_generic_filename + '.png'


class ImageTests(TestCase):

    @classmethod
    def setUpClass(cls):
        script_path = os.path.realpath(__file__)
        test_dir_path = os.path.dirname(script_path)
        cls.image_path = os.path.join(test_dir_path, 'pygame2')

    def get_image_path(self, extension):
        return self.image_path + extension

    def assertIsValidSurface(self, surface):
        self.assertIsInstance(surface, pygame2.surface.Surface)
        self.assertGreater(surface.get_width(), 0)
        self.assertGreater(surface.get_height(), 0)

# def test_frombuffer(self):
#         self.fail()
