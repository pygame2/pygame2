    # These are integration tests, not a unit tests
    # ###########################################################
    # def _test_load_file(self, filename):
    #     surface = pygame2.image.load(filename)
    #     self.assertIsValidSurface(surface)
    #     with open(filename, 'rb') as fh:
    #         surface = pygame2.image.load(fh, filename)
    #         self.assertIsValidSurface(surface)
    #
    # def test_load_jpg(self):
    #     self._test_load_file(default_generic_filename + '.jpg')
    #
    # def test_load_png(self):
    #     self._test_load_file(default_generic_filename + '.png')
    #
    # def test_load_gif(self):
    #     self._test_load_file(default_generic_filename + '.gif')
    #
    # def test_load_bmp(self):
    #     self._test_load_file(default_generic_filename + '.bmp')
    #
    # def _test_save_file(self, extension):
    #     test_filename = 'test_save' + extension
    #     fmt = 'ARGB'
    #     original = pygame2.image.load(default_filename)
    #     pygame2.image.save(original, test_filename)
    #     surface = pygame2.image.load(test_filename)
    #     os.unlink(test_filename)
    #     self.assertEqual(pygame2.image.tostring(original, fmt),
    #                      pygame2.image.tostring(surface, fmt))
    #
    # def test_save_png(self):
    #     self._test_save_file('.png')
    #
    # def test_save_bmp(self):
    #     self._test_save_file('.bmp')
    #
    # def test_save_gif(self):
    #     self._test_save_file('.gif')
    #
    # def test_save_jpg(self):
    #     self._test_save_file('.jpg')
    #
    # def test_get_extended(self):
    #         self.fail()
    #
    # def test_tostring_all_formats(self):
    #     surface = pygame2.core.image.image.load(self.get_image_path('.png'))
    #     for fmt in supported_formats:
    #         pygame2.core.image.image.tostring(surface, fmt)
    #
    # def test_tostring_fromstring(self):
    #     fmt = 'ARGB'
    #     original = pygame2.core.image.image.load(self.get_image_path('.png'))
    #     size = original.get_size()
    #     data = pygame2.core.image.image.tostring(original, fmt)
    #     surface2 = pygame2.core.image.image.fromstring(data, size, fmt)
    #     self.assertEqual(data, pygame2.core.image.image.tostring(surface2, fmt))
    #     self.assertEqual(pygame2.core.image.image.tostring(original, fmt),
    #                      pygame2.core.image.image.tostring(surface2, fmt))
    # # ###########################################################