"""
massaged to work with pygame2 2 from the pygame2 project
unknown licence, assuming LGPL
"""

# import math
# import unittest

# import pygame2
# #from pygame2.compat import long_
# long_ = int


# rgba_vals = [0, 1, 62, 63, 126, 127, 255]

# rgba_combinations = [(r, g, b, a) for r in rgba_vals
#                      for g in rgba_vals
#                      for b in rgba_vals
#                      for a in rgba_vals]

# # ##############################################################################

# def rgba_combos_Color_generator():
#     for rgba in rgba_combinations:
#         yield pygame2.Color(*rgba)


# # Python gamma correct
# def gamma_correct(rgba_0_255, gamma):
#     corrected = round(255.0 * math.pow(rgba_0_255 / 255.0, gamma))
#     return max(min(int(corrected), 255), 0)


# ################################################################################

# # TODO: add tests for
# # correct_gamma()  -- test against statically defined verified correct values
# # coerce ()        --  ??

# def _assignr(x, y):
#     x.r = y


# def _assigng(x, y):
#     x.g = y


# def _assignb(x, y):
#     x.b = y


# def _assigna(x, y):
#     x.a = y


# def _assign_item(x, p, y):
#     x[p] = y


# class ColorTypeTest(unittest.TestCase):
#     def test_invalid_html_hex_codes(self):
#         # This was a problem with the way 2 digit hex numbers were
#         # calculated. The test_hex_digits test is related to the fix.
#         Color = pygame2.color.Color
#         self.failUnlessRaises(ValueError, lambda: Color('# f000000'))
#         self.failUnlessRaises(ValueError, lambda: Color('#f 000000'))
#         self.failUnlessRaises(ValueError, lambda: Color('#-f000000'))

#     def test_hex_digits(self):
#         # This is an implementation specific test.
#         # Two digit hex numbers are calculated using table lookups
#         # for the upper and lower digits.
#         Color = pygame2.color.Color
#         self.assertEqual(Color('#00000000').r, 0x00)
#         self.assertEqual(Color('#10000000').r, 0x10)
#         self.assertEqual(Color('#20000000').r, 0x20)
#         self.assertEqual(Color('#30000000').r, 0x30)
#         self.assertEqual(Color('#40000000').r, 0x40)
#         self.assertEqual(Color('#50000000').r, 0x50)
#         self.assertEqual(Color('#60000000').r, 0x60)
#         self.assertEqual(Color('#70000000').r, 0x70)
#         self.assertEqual(Color('#80000000').r, 0x80)
#         self.assertEqual(Color('#90000000').r, 0x90)
#         self.assertEqual(Color('#A0000000').r, 0xA0)
#         self.assertEqual(Color('#B0000000').r, 0xB0)
#         self.assertEqual(Color('#C0000000').r, 0xC0)
#         self.assertEqual(Color('#D0000000').r, 0xD0)
#         self.assertEqual(Color('#E0000000').r, 0xE0)
#         self.assertEqual(Color('#F0000000').r, 0xF0)
#         self.assertEqual(Color('#01000000').r, 0x01)
#         self.assertEqual(Color('#02000000').r, 0x02)
#         self.assertEqual(Color('#03000000').r, 0x03)
#         self.assertEqual(Color('#04000000').r, 0x04)
#         self.assertEqual(Color('#05000000').r, 0x05)
#         self.assertEqual(Color('#06000000').r, 0x06)
#         self.assertEqual(Color('#07000000').r, 0x07)
#         self.assertEqual(Color('#08000000').r, 0x08)
#         self.assertEqual(Color('#09000000').r, 0x09)
#         self.assertEqual(Color('#0A000000').r, 0x0A)
#         self.assertEqual(Color('#0B000000').r, 0x0B)
#         self.assertEqual(Color('#0C000000').r, 0x0C)
#         self.assertEqual(Color('#0D000000').r, 0x0D)
#         self.assertEqual(Color('#0E000000').r, 0x0E)
#         self.assertEqual(Color('#0F000000').r, 0x0F)

#     def test_comparison(self):
#         Color = pygame2.color.Color

#         # Check valid comparisons
#         self.failUnless(Color(255, 0, 0, 0) == Color(255, 0, 0, 0))
#         self.failUnless(Color(0, 255, 0, 0) == Color(0, 255, 0, 0))
#         self.failUnless(Color(0, 0, 255, 0) == Color(0, 0, 255, 0))
#         self.failUnless(Color(0, 0, 0, 255) == Color(0, 0, 0, 255))
#         self.failIf(Color(0, 0, 0, 0) == Color(255, 0, 0, 0))
#         self.failIf(Color(0, 0, 0, 0) == Color(0, 255, 0, 0))
#         self.failIf(Color(0, 0, 0, 0) == Color(0, 0, 255, 0))
#         self.failIf(Color(0, 0, 0, 0) == Color(0, 0, 0, 255))
#         self.failUnless(Color(0, 0, 0, 0) != Color(255, 0, 0, 0))
#         self.failUnless(Color(0, 0, 0, 0) != Color(0, 255, 0, 0))
#         self.failUnless(Color(0, 0, 0, 0) != Color(0, 0, 255, 0))
#         self.failUnless(Color(0, 0, 0, 0) != Color(0, 0, 0, 255))
#         self.failIf(Color(255, 0, 0, 0) != Color(255, 0, 0, 0))
#         self.failIf(Color(0, 255, 0, 0) != Color(0, 255, 0, 0))
#         self.failIf(Color(0, 0, 255, 0) != Color(0, 0, 255, 0))
#         self.failIf(Color(0, 0, 0, 255) != Color(0, 0, 0, 255))

#         self.failUnless(Color(255, 0, 0, 0) == (255, 0, 0, 0))
#         self.failUnless(Color(0, 255, 0, 0) == (0, 255, 0, 0))
#         self.failUnless(Color(0, 0, 255, 0) == (0, 0, 255, 0))
#         self.failUnless(Color(0, 0, 0, 255) == (0, 0, 0, 255))
#         self.failIf(Color(0, 0, 0, 0) == (255, 0, 0, 0))
#         self.failIf(Color(0, 0, 0, 0) == (0, 255, 0, 0))
#         self.failIf(Color(0, 0, 0, 0) == (0, 0, 255, 0))
#         self.failIf(Color(0, 0, 0, 0) == (0, 0, 0, 255))
#         self.failUnless(Color(0, 0, 0, 0) != (255, 0, 0, 0))
#         self.failUnless(Color(0, 0, 0, 0) != (0, 255, 0, 0))
#         self.failUnless(Color(0, 0, 0, 0) != (0, 0, 255, 0))
#         self.failUnless(Color(0, 0, 0, 0) != (0, 0, 0, 255))
#         self.failIf(Color(255, 0, 0, 0) != (255, 0, 0, 0))
#         self.failIf(Color(0, 255, 0, 0) != (0, 255, 0, 0))
#         self.failIf(Color(0, 0, 255, 0) != (0, 0, 255, 0))
#         self.failIf(Color(0, 0, 0, 255) != (0, 0, 0, 255))

#         self.failUnless((255, 0, 0, 0) == Color(255, 0, 0, 0))
#         self.failUnless((0, 255, 0, 0) == Color(0, 255, 0, 0))
#         self.failUnless((0, 0, 255, 0) == Color(0, 0, 255, 0))
#         self.failUnless((0, 0, 0, 255) == Color(0, 0, 0, 255))
#         self.failIf((0, 0, 0, 0) == Color(255, 0, 0, 0))
#         self.failIf((0, 0, 0, 0) == Color(0, 255, 0, 0))
#         self.failIf((0, 0, 0, 0) == Color(0, 0, 255, 0))
#         self.failIf((0, 0, 0, 0) == Color(0, 0, 0, 255))
#         self.failUnless((0, 0, 0, 0) != Color(255, 0, 0, 0))
#         self.failUnless((0, 0, 0, 0) != Color(0, 255, 0, 0))
#         self.failUnless((0, 0, 0, 0) != Color(0, 0, 255, 0))
#         self.failUnless((0, 0, 0, 0) != Color(0, 0, 0, 255))
#         self.failIf((255, 0, 0, 0) != Color(255, 0, 0, 0))
#         self.failIf((0, 255, 0, 0) != Color(0, 255, 0, 0))
#         self.failIf((0, 0, 255, 0) != Color(0, 0, 255, 0))
#         self.failIf((0, 0, 0, 255) != Color(0, 0, 0, 255))

#         class TupleSubclass(tuple):
#             pass

#         self.failUnless(Color(255, 0, 0, 0) == TupleSubclass((255, 0, 0, 0)))
#         self.failUnless(TupleSubclass((255, 0, 0, 0)) == Color(255, 0, 0, 0))
#         self.failIf(Color(255, 0, 0, 0) != TupleSubclass((255, 0, 0, 0)))
#         self.failIf(TupleSubclass((255, 0, 0, 0)) != Color(255, 0, 0, 0))

#         # These are not supported so will be unequal.
#         self.failIf(Color(255, 0, 0, 0) == "#ff000000")
#         self.failUnless(Color(255, 0, 0, 0) != "#ff000000")

#         self.failIf("#ff000000" == Color(255, 0, 0, 0))
#         self.failUnless("#ff000000" != Color(255, 0, 0, 0))

#         self.failIf(Color(255, 0, 0, 0) == 0xff000000)
#         self.failUnless(Color(255, 0, 0, 0) != 0xff000000)

#         self.failIf(0xff000000 == Color(255, 0, 0, 0))
#         self.failUnless(0xff000000 != Color(255, 0, 0, 0))

#         self.failIf(Color(255, 0, 0, 0) == [255, 0, 0, 0])
#         self.failUnless(Color(255, 0, 0, 0) != [255, 0, 0, 0])

#         self.failIf([255, 0, 0, 0] == Color(255, 0, 0, 0))
#         self.failUnless([255, 0, 0, 0] != Color(255, 0, 0, 0))

#         # Comparison is not implemented for invalid color values.
#         class Test(object):
#             def __eq__(self, other):
#                 return -1

#             def __ne__(self, other):
#                 return -2

#         class TestTuple(tuple):
#             def __eq__(self, other):
#                 return -1

#             def __ne__(self, other):
#                 return -2

#         t = Test()
#         t_tuple = TestTuple(('a', 0, 0, 0))
#         black = Color('black')

#         self.assertEqual(black == t, False)
#         self.assertEqual(t == black, -1)
#         self.assertEqual(black != t, True)
#         self.assertEqual(t != black, -2)
#         self.assertEqual(black == t_tuple, False)
#         self.assertEqual(black != t_tuple, True)
#         self.assertEqual(t_tuple == black, -1)
#         self.assertEqual(t_tuple != black, -2)

#     def test_arg_lengths(self):
#         """Test the number and type of args sent"""
#         Color = pygame2.Color

#         # Test 4 arguments
#         c = Color(255, 0, 0, 202)
#         self.assertEqual(c, (255, 0, 0, 202))
#         self.assertEqual(len(c), 4)

#         # Test 3 arguments
#         c = Color(255, 0, 0)
#         self.assertEqual(c, (255, 0, 0, 255))
#         self.assertEqual(len(c), 3)

#         # Test 1 argument name
#         c = Color('pink')
#         self.assertEqual(c, (255, 192, 203, 255))
#         self.assertEqual(len(c), 4)

#         # Test 1 argument object
#         c2 = Color(c)
#         self.failIf(c is c2)
#         self.assertEqual(c2, c)
#         self.assertEqual(c2.length, 4)

#         # Test 0 argument object
#         c = Color()
#         self.assertEqual(c, (0, 0, 0, 255))
#         self.assertEqual(c2.length, 4)

#         # Test too many arguments
#         self.assertRaises(ValueError, Color, 0, 0, 0, 0, 0)

#     def test_iter(self):
#         """Make sure the iterables work"""
#         Color = pygame2.Color

#         # Test 4 length
#         c = Color(1, 2, 3, 4)
#         self.assertEqual([i for i in c], [1, 2, 3, 4])
#         self.assertEqual([i for i in reversed(c)], [4, 3, 2, 1])

#         # Test 3 length
#         c.length = 3
#         self.assertEqual([i for i in c], [1, 2, 3])
#         self.assertEqual([i for i in reversed(c)], [3, 2, 1])

#         # Test 2 length
#         c.length = 2
#         self.assertEqual([i for i in c], [1, 2])
#         self.assertEqual([i for i in reversed(c)], [2, 1])

#         # Test 1 length
#         c.length = 1
#         self.assertEqual([i for i in c], [1])
#         self.assertEqual([i for i in reversed(c)], [1])

#     def test_copy(self):
#         from copy import copy
#         Color = pygame2.Color

#         c = Color(1, 2, 3, 4)

#         c1 = copy(c)
#         self.assertEqual(c1, (1, 2, 3, 4))

#         c.length = 3
#         c1 = copy(c)
#         self.assertEqual(c1, (1, 2, 3))

#         c.length = 2
#         c1 = copy(c)
#         self.assertEqual(c1, (1, 2))

#         c.length = 1
#         c1 = copy(c)
#         self.assertEqual(c1, 1)

#     def test_str(self):
#         for color in pygame2.color.colors:
#             self.assertEquals(str(pygame2.color.Color(color)),
#                               "Color(r={0}, g={1}, b={2}, a={3})".format(
#                                   *pygame2.color.colors[color]))

#     def test_ignore_whitespace(self):
#         self.assertEquals(pygame2.color.Color('red'),
#                           pygame2.color.Color(' r e d '))

#     def test_slice(self):
#         #"""|tags: python3_ignore|"""

#         # slicing a color gives you back a tuple.
#         # do all sorts of slice combinations.
#         c = pygame2.Color(1, 2, 3, 4)

#         self.assertEquals((1, 2, 3, 4), c[:])
#         self.assertEquals((1, 2, 3), c[:-1])

#         self.assertEquals((), c[:-5])

#         self.assertEquals((1, 2, 3, 4), c[:4])
#         self.assertEquals((1, 2, 3, 4), c[:5])
#         self.assertEquals((1, 2), c[:2])
#         self.assertEquals((1,), c[:1])
#         self.assertEquals((), c[:0])

#         self.assertEquals((2,), c[1:-2])
#         self.assertEquals((3, 4), c[-2:])
#         self.assertEquals((4,), c[-1:])

#         # NOTE: assigning to a slice is currently unsupported.

#     def test_unpack(self):
#         # should be able to unpack to r,g,b,a and r,g,b
#         c = pygame2.Color(1, 2, 3, 4)
#         r, g, b, a = c
#         self.assertEquals((1, 2, 3, 4), (r, g, b, a))
#         self.assertEquals(c, (r, g, b, a))

#         c.set_length(3)
#         r, g, b = c
#         self.assertEquals((1, 2, 3), (r, g, b))

#     def test_length(self):
#         # should be able to unpack to r,g,b,a and r,g,b
#         c = pygame2.Color(1, 2, 3, 4)
#         self.assertEquals(len(c), 4)

#         c.set_length(3)
#         self.assertEquals(len(c), 3)

#         # it keeps the old alpha anyway...
#         self.assertEquals(c.a, 4)

#         # however you can't get the alpha in this way:
#         self.assertRaises(IndexError, lambda x: c[x], 4)

#         c.set_length(4)
#         self.assertEquals(len(c), 4)

#         self.assertRaises(ValueError, c.set_length, 5)
#         self.assertRaises(ValueError, c.set_length, -1)
#         self.assertRaises(ValueError, c.set_length, 0)
#         self.assertRaises(ValueError, c.set_length, pow(2, long_(33)))

#     def test_case_insensitivity_of_string_args(self):
#         self.assertEquals(pygame2.color.Color('red'), pygame2.color.Color('Red'))

#     def test_color(self):
#         c = pygame2.Color(10, 20, 30, 40)
#         self.assertEquals(c, (10, 20, 30, 40))

#         c = pygame2.Color("indianred3")
#         self.assertEquals(c, (205, 85, 85, 255))

#         c = pygame2.Color('0xAABBCCDD')
#         self.assertEquals(c, (0xAA, 0xBB, 0xCC, 0xDD))

#         self.assertRaises(ValueError, pygame2.Color, 257, 10, 105, 44)
#         self.assertRaises(ValueError, pygame2.Color, 10, 257, 105, 44)
#         self.assertRaises(ValueError, pygame2.Color, 10, 105, 257, 44)
#         self.assertRaises(ValueError, pygame2.Color, 10, 105, 44, 257)

#     def test_rgba(self):
#         c = pygame2.Color(0)

#         # Test simple assignments
#         c.r = 123
#         self.assertRaises(ValueError, _assignr, c, 537)
#         self.assertRaises(ValueError, _assignr, c, -3)
#         self.assertEquals(c.r, 123)

#         c.g = 55
#         self.assertRaises(ValueError, _assigng, c, 348)
#         self.assertRaises(ValueError, _assigng, c, -44)
#         self.assertEquals(c.g, 55)

#         c.b = 77
#         self.assertRaises(ValueError, _assignb, c, 256)
#         self.assertRaises(ValueError, _assignb, c, -12)
#         self.assertEquals(c.b, 77)

#         c.a = 255
#         self.assertRaises(ValueError, _assigna, c, 312)
#         self.assertRaises(ValueError, _assigna, c, -10)
#         self.assertEquals(c.a, 255)

#     def test_repr(self):
#         for color in pygame2.color.colors:
#             self.assertEquals(repr(pygame2.color.Color(color)),
#                               "({0}, {1}, {2}, {3})".format(
#                                   *pygame2.color.colors[color]))

#     def test_add(self):
#         c1 = pygame2.Color(0)

#         c2 = pygame2.Color(20, 33, 82, 193)

#         c3 = c1 + c2
#         self.assertEquals(c3, (20, 33, 82, 193))

#         c3 += c2
#         self.assertEquals(c3, (40, 66, 164, 255))

#     def test_sub(self):
#         c1 = pygame2.Color(0xFFFFFFFF)
#         c2 = pygame2.Color(20, 33, 82, 193)

#         c3 = c1 - c2
#         self.assertEquals(c3, (235, 222, 173, 62))

#         c3 -= c2
#         self.assertEquals(c3, (215, 189, 91, 0))

#     def test_mul(self):
#         c1 = pygame2.Color(0x01010101)
#         c2 = pygame2.Color(2, 5, 3, 22)

#         c3 = c1 * c2
#         self.assertEquals(c3, (2, 5, 3, 22))

#         c3 *= c2
#         self.assertEquals(c3, (4, 25, 9, 255))

#     def test_floordiv(self):
#         c1 = pygame2.Color('0x80808080')
#         c2 = pygame2.Color(2, 4, 8, 16)

#         c3 = c1 // c2
#         self.assertEquals(c3, (64, 32, 16, 8))

#         c3 = c3 // c2
#         self.assertEquals(c3, (32, 8, 2, 0))

#         c4 = pygame2.color.Color(0, 0, 0, 0)

#         c3 //= c4
#         self.assertEquals(c3, (32, 8, 2, 0))

#     def test_div(self):
#         c1 = pygame2.Color('0x80808080')
#         c2 = pygame2.Color(2, 4, 8, 16)

#         c3 = c1 / c2
#         self.assertEquals(c3, (64, 32, 16, 8))

#         c3 = c3 / c2
#         self.assertEquals(c3, (32, 8, 2, 0))

#         c4 = pygame2.color.Color(0, 0, 0, 0)

#         c3 /= c4
#         self.assertEquals(c3, (32, 8, 2, 0))

#     def test_mod(self):
#         c1 = pygame2.Color('0xFFFFFFFF')
#         c2 = pygame2.Color(2, 4, 8, 16)

#         c3 = c1 % c2
#         self.assertEquals(c3, (1, 3, 7, 15))

#     def test_float(self):
#         c = pygame2.Color('0xCC00CC00')
#         self.assertEquals(c, (204, 0, 204, 0))
#         self.assertEquals(float(c), float(0xCC00CC00))

#         c = pygame2.Color('0x33727592')
#         self.assertEquals(c, (51, 114, 117, 146))
#         self.assertEquals(float(c), float(0x33727592))

#     def test_oct(self):
#         c = pygame2.Color('0xCC00CC00')
#         self.assertEquals(c, (204, 0, 204, 0))
#         self.assertEquals(oct(c), oct(0xCC00CC00))

#         c = pygame2.Color('0x33727592')
#         self.assertEquals(c, (51, 114, 117, 146))
#         self.assertEquals(oct(c), oct(0x33727592))

#     def test_hex(self):
#         c = pygame2.Color('0xCC00CC00')
#         self.assertEquals(c, (204, 0, 204, 0))
#         self.assertEquals(hex(c), hex(0xCC00CC00))

#         c = pygame2.Color('0x33727592')
#         self.assertEquals(c, (51, 114, 117, 146))
#         self.assertEquals(hex(c), hex(0x33727592))

#         c = pygame2.Color("0xCC00CC")
#         self.assertEquals(c, (204, 0, 204, 255))
#         self.assertEquals(hex(c), hex(0xCC00CCFF))

#         self.assertRaises(ValueError, pygame2.Color, "0xcc00qq")

#     def test_webstyle(self):
#         c = pygame2.Color("#CC00CC11")
#         self.assertEquals(c, (204, 0, 204, 17))

#         c = pygame2.Color("#CC00CC")
#         self.assertEquals(c, (204, 0, 204, 255))

#         c = pygame2.Color("0xCC00CC11")
#         self.assertEquals(c, (204, 0, 204, 17))

#         self.assertRaises(ValueError, pygame2.Color, "#cc00qq")
#         self.assertRaises(ValueError, pygame2.Color, "09abcdef")
#         self.assertRaises(ValueError, pygame2.Color, "09abcde")
#         self.assertRaises(ValueError, pygame2.Color, "quarky")

#     def test_int(self):
#         # This will be a long
#         c = pygame2.Color('0xCC00CC00')
#         self.assertEquals(c.r, 204)
#         self.assertEquals(c.g, 0)
#         self.assertEquals(c.b, 204)
#         self.assertEquals(c.a, 0)
#         self.assertEquals(int(c), int(0xCC00CC00))

#         # This will be an int
#         c = pygame2.Color('0x33727592')
#         self.assertEquals(c.r, 51)
#         self.assertEquals(c.g, 114)
#         self.assertEquals(c.b, 117)
#         self.assertEquals(c.a, 146)
#         self.assertEquals(int(c), int(0x33727592))

#     def test_long(self):
#         # This will be a long
#         c = pygame2.Color('0xCC00CC00')
#         self.assertEquals(c.r, 204)
#         self.assertEquals(c.g, 0)
#         self.assertEquals(c.b, 204)
#         self.assertEquals(c.a, 0)
#         self.assertEquals(long_(c), long_(0xCC00CC00))

#         # This will be an int
#         c = pygame2.Color('0x33727592')
#         self.assertEquals(c.r, 51)
#         self.assertEquals(c.g, 114)
#         self.assertEquals(c.b, 117)
#         self.assertEquals(c.a, 146)
#         self.assertEquals(long_(c), long_(0x33727592))

#     def test_normalize(self):
#         c = pygame2.Color(204, 38, 194, 55)
#         self.assertEquals(c.r, 204)
#         self.assertEquals(c.g, 38)
#         self.assertEquals(c.b, 194)
#         self.assertEquals(c.a, 55)

#         t = c.normalize()

#         self.assertAlmostEquals(t[0], 0.800000, 5)
#         self.assertAlmostEquals(t[1], 0.149016, 5)
#         self.assertAlmostEquals(t[2], 0.760784, 5)
#         self.assertAlmostEquals(t[3], 0.215686, 5)

#     def test_len(self):
#         c = pygame2.Color(204, 38, 194, 55)
#         self.assertEquals(len(c), 4)

#     def test_get_item(self):
#         c = pygame2.Color(204, 38, 194, 55)
#         self.assertEquals(c[0], 204)
#         self.assertEquals(c[1], 38)
#         self.assertEquals(c[2], 194)
#         self.assertEquals(c[3], 55)

#     def test_set_item(self):
#         c = pygame2.Color()

#         c[0] = 33
#         self.assertEquals(c[0], 33)
#         c[1] = 48
#         self.assertEquals(c[1], 48)
#         c[2] = 173
#         self.assertEquals(c[2], 173)
#         c[3] = 213
#         self.assertEquals(c[3], 213)

#         # Now try some 'invalid' ones
#         for i in range(4):
#             self.assertRaises(ValueError, _assign_item, c, i, -83)
#             self.assertRaises(TypeError, _assign_item, c, i, "Hello")
#             self.assertRaises(TypeError, _assign_item, c, i, 95.485)
#         self.assertEquals(c[0], 33)
#         self.assertEquals(c[1], 48)
#         self.assertEquals(c[2], 173)
#         self.assertEquals(c[3], 213)

#     def test_Color_type_works_for_Surface_get_and_set_colorkey(self):
#         s = pygame2.Surface((32, 32))

#         c = pygame2.Color(33, 22, 11, 255)
#         s.set_colorkey(c)

#         get_r, get_g, get_b, get_a = s.get_colorkey()

#         self.assert_(get_r == c.r)
#         self.assert_(get_g == c.g)
#         self.assert_(get_b == c.b)
#         self.assert_(get_a == c.a)

#     ########## HSLA, HSVA, CMY, I1I2I3 ALL ELEMENTS WITHIN SPECIFIED RANGE
#     # #########

#     def test_hsla__all_elements_within_limits(self):
#         for c in rgba_combos_Color_generator():
#             h, s, l, a = c.hsla
#             self.assert_(0 <= h <= 360)
#             self.assert_(0 <= s <= 100)
#             self.assert_(0 <= l <= 100)
#             self.assert_(0 <= a <= 100)

#     def test_hsva__all_elements_within_limits(self):
#         for c in rgba_combos_Color_generator():
#             h, s, v, a = c.hsva
#             self.assert_(0 <= h <= 360)
#             self.assert_(0 <= s <= 100)
#             self.assert_(0 <= v <= 100)
#             self.assert_(0 <= a <= 100)

#     def test_valid_hsva(self):
#         c = pygame2.Color('pink')
#         c.hsva = (359, c.hsva[1], c.hsva[2], c.hsva[3])
#         self.assert_(0 <= c.hsva[0] <= 360)

#     def test_invalid_hsva(self):
#         for h in (-1, 361):
#             try:
#                 pygame2.Color().hsva = (h, 0, 0, 0)
#                 self.assertFalse(False)
#             except ValueError:
#                 pass

#     def test_cmy__all_elements_within_limits(self):
#         for c in rgba_combos_Color_generator():
#             c, m, y = c.cmy
#             self.assert_(0 <= c <= 1)
#             self.assert_(0 <= m <= 1)
#             self.assert_(0 <= y <= 1)

#     def test_i1i2i3__all_elements_within_limits(self):
#         for c in rgba_combos_Color_generator():
#             i1, i2, i3 = c.i1i2i3
#             self.assert_(0 <= i1 <= 1)
#             self.assert_(-0.5 <= i2 <= 0.5)
#             self.assert_(-0.5 <= i3 <= 0.5)

#         ####################### COLORSPACE PROPERTY SANITY TESTS
#         # #######################

#     def colorspaces_converted_should_not_raise(self, prop):
#         fails = 0

#         x = 0
#         for c in rgba_combos_Color_generator():
#             x += 1

#             other = pygame2.Color(0)

#             try:
#                 setattr(other, prop, getattr(c, prop))
#                 #eg other.hsla = c.hsla

#             except ValueError:
#                 fails += 1

#         self.assert_(x > 0, "x is combination counter, 0 means no tests!")
#         self.assert_((fails, x) == (0, x))

#     def test_hsla__sanity_testing_converted_should_not_raise(self):
#         self.colorspaces_converted_should_not_raise('hsla')

#     def test_hsva__sanity_testing_converted_should_not_raise(self):
#         self.colorspaces_converted_should_not_raise('hsva')

#     def test_cmy__sanity_testing_converted_should_not_raise(self):
#         self.colorspaces_converted_should_not_raise('cmy')

#     def test_i1i2i3__sanity_testing_converted_should_not_raise(self):
#         self.colorspaces_converted_should_not_raise('i1i2i3')

#     ############################################################################

#     def colorspaces_converted_should_equate_bar_rounding(self, prop):
#         for c in rgba_combos_Color_generator():
#             other = pygame2.Color(0)

#             try:
#                 setattr(other, prop, getattr(c, prop))
#                 #eg other.hsla = c.hsla

#                 self.assert_(abs(other.r - c.r) <= 1)
#                 self.assert_(abs(other.b - c.b) <= 1)
#                 self.assert_(abs(other.g - c.g) <= 1)
#                 # CMY and I1I2I3 do not care about the alpha
#                 if not prop in ("cmy", "i1i2i3"):
#                     self.assert_(abs(other.a - c.a) <= 1)

#             except ValueError:
#                 pass  # other tests will notify, this tests equation

#     def test_hsla__sanity_testing_converted_should_equate_bar_rounding(self):
#         self.colorspaces_converted_should_equate_bar_rounding('hsla')

#     def test_hsva__sanity_testing_converted_should_equate_bar_rounding(self):
#         self.colorspaces_converted_should_equate_bar_rounding('hsva')

#     def test_cmy__sanity_testing_converted_should_equate_bar_rounding(self):
#         self.colorspaces_converted_should_equate_bar_rounding('cmy')

#     def test_i1i2i3__sanity_testing_converted_should_equate_bar_rounding(self):
#         self.colorspaces_converted_should_equate_bar_rounding('i1i2i3')

#     ################################################################################

#     def test_correct_gamma__verified_against_python_implementation(self):
#         """|tags:slow|"""
#         # gamma_correct defined at top of page

#         gammas = [i / 10.0 for i in range(1, 31)]  # [0.1 ... 3.0]
#         gammas_len = len(gammas)

#         for i, c in enumerate(rgba_combos_Color_generator()):
#             gamma = gammas[i % gammas_len]

#             corrected = pygame2.Color(*[gamma_correct(x, gamma)
#                                         for x in tuple(c)])
#             lib_corrected = c.correct_gamma(gamma)

#             self.assert_(corrected.r == lib_corrected.r)
#             self.assert_(corrected.g == lib_corrected.g)
#             self.assert_(corrected.b == lib_corrected.b)
#             self.assert_(corrected.a == lib_corrected.a)

#             # TODO: test against statically defined verified _correct_ values
#             # assert corrected.r == 125 etc.

#     def test_pickle(self):
#         import pickle

#         c1 = pygame2.Color(1, 2, 3, 4)
#         #c2 = pygame2.Color(255,254,253,252)
#         pickle_string = pickle.dumps(c1)
#         c1_frompickle = pickle.loads(pickle_string)
#         self.assertEqual(c1, c1_frompickle)

#     ############################################################################
#     # only available if ctypes module is also available

#     def test_arraystruct(self):
#         import pygame2.tests.test_utils.arrinter as ai
#         import ctypes as ct

#         c_byte_p = ct.POINTER(ct.c_byte)
#         c = pygame2.Color(5, 7, 13, 23)
#         flags = (ai.PAI_CONTIGUOUS | ai.PAI_FORTRAN |
#                  ai.PAI_ALIGNED | ai.PAI_NOTSWAPPED)
#         for i in range(1, 5):
#             c.set_length(i)
#             inter = ai.ArrayInterface(c)
#             self.assertEqual(inter.two, 2)
#             self.assertEqual(inter.nd, 1)
#             self.assertEqual(inter.typekind, 'u')
#             self.assertEqual(inter.itemsize, 1)
#             self.assertEqual(inter.flags, flags)
#             self.assertEqual(inter.shape[0], i)
#             self.assertEqual(inter.strides[0], 1)
#             data = ct.cast(inter.data, c_byte_p)
#             for j in range(i):
#                 self.assertEqual(data[j], c[j])

#     try:
#         # TODO: Actually implement this flag to test against :P
#         if pygame2.HAVE_NEWBUF:
#             def test_newbuf(self):
#                 self.NEWBUF_test_newbuf()

#             if is_pygame2_pkg:
#                 from pygame2.tests.test_utils import buftools
#             else:
#                 from test.test_utils import buftools
#     except AttributeError:
#         pass

#     def NEWBUF_test_newbuf(self):
#         from ctypes import cast, POINTER, c_uint8

#         buftools = self.buftools

#         class ColorImporter(buftools.Importer):
#             def __init__(self, color, flags):
#                 super(ColorImporter, self).__init__(color, flags)
#                 self.items = cast(self.buf, POINTER(c_uint8))

#             def __getitem__(self, index):
#                 if 0 <= index < 4:
#                     return self.items[index]
#                 raise IndexError("valid index values are between 0 and 3: "
#                                  "got {}".format(index))

#             def __setitem__(self, index, value):
#                 if 0 <= index < 4:
#                     self.items[index] = value
#                 else:
#                     raise IndexError("valid index values are between 0 and 3: "
#                                      "got {}".format(index))

#         c = pygame2.Color(50, 100, 150, 200)
#         imp = ColorImporter(c, buftools.PyBUF_SIMPLE)
#         self.assertTrue(imp.obj is c)
#         self.assertEqual(imp.ndim, 0)
#         self.assertEqual(imp.itemsize, 1)
#         self.assertEqual(imp.len, 4)
#         self.assertTrue(imp.readonly)
#         self.assertTrue(imp.format is None)
#         self.assertTrue(imp.shape is None)
#         self.assertTrue(imp.strides is None)
#         self.assertTrue(imp.suboffsets is None)
#         for i in range(4):
#             self.assertEqual(c[i], imp[i])
#         imp[0] = 60
#         self.assertEqual(c.r, 60)
#         imp[1] = 110
#         self.assertEqual(c.g, 110)
#         imp[2] = 160
#         self.assertEqual(c.b, 160)
#         imp[3] = 210
#         self.assertEqual(c.a, 210)
#         imp = ColorImporter(c, buftools.PyBUF_FORMAT)
#         self.assertEqual(imp.ndim, 0)
#         self.assertEqual(imp.itemsize, 1)
#         self.assertEqual(imp.len, 4)
#         self.assertEqual(imp.format, 'B')
#         self.assertEqual(imp.ndim, 0)
#         self.assertEqual(imp.itemsize, 1)
#         self.assertEqual(imp.len, 4)
#         imp = ColorImporter(c, buftools.PyBUF_ND)
#         self.assertEqual(imp.ndim, 1)
#         self.assertEqual(imp.itemsize, 1)
#         self.assertEqual(imp.len, 4)
#         self.assertTrue(imp.format is None)
#         self.assertEqual(imp.shape, (4,))
#         self.assertEqual(imp.strides, None)
#         imp = ColorImporter(c, buftools.PyBUF_STRIDES)
#         self.assertEqual(imp.ndim, 1)
#         self.assertTrue(imp.format is None)
#         self.assertEqual(imp.shape, (4,))
#         self.assertEqual(imp.strides, (1,))
#         imp = ColorImporter(c, buftools.PyBUF_C_CONTIGUOUS)
#         self.assertEqual(imp.ndim, 1)
#         imp = ColorImporter(c, buftools.PyBUF_F_CONTIGUOUS)
#         self.assertEqual(imp.ndim, 1)
#         imp = ColorImporter(c, buftools.PyBUF_ANY_CONTIGUOUS)
#         self.assertEqual(imp.ndim, 1)
#         for i in range(1, 5):
#             c.set_length(i)
#             imp = ColorImporter(c, buftools.PyBUF_ND)
#             self.assertEqual(imp.ndim, 1)
#             self.assertEqual(imp.len, i)
#             self.assertEqual(imp.shape, (i,))
#         self.assertRaises(BufferError, ColorImporter,
#                           c, buftools.PyBUF_WRITABLE)

#     try:
#         import ctypes
#     except ImportError:
#         del test_arraystruct


# ################################################################################

# if __name__ == '__main__':
#     unittest.main()
