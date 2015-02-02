"""
"""
from math import floor, pow
import re

__all__ = ["Color", "gamma_decode", "is_rgb_color", "is_rgba_color",
           "argb_to_color", "ARGB", "rgba_to_color", "RGBA", "string_to_color",
           "convert_to_color", "COLOR"]

long = int


class Color:
    """Color(red, green, blue, alpha)

    Color(red, green, blue)

    Color(name)

    Color("#rrggbbaa")

    Color("0xrrggbbaa")

    Color(argb_int)

    Color(argb_hex)

    Color(object)

    Color() -> Color('black')

    Args:
        args (tuple): red, green, blue [, alpha].  See argb_to_color().

        args (string): Color name from pygame2.color.colors

        args (string): HTML or hex color string.  See string_to_color().
    """

    def __init__(self, *args):
        self._length = 4
        if len(args) == 4:
            r, g, b, a = args
        elif len(args) == 3:
            r, g, b = args
            a = 255
            self._length = 3
        elif len(args) == 1 \
                and hasattr(args[0], 'lower') \
                and re.sub(r'\s+', '', args[0].lower()) in colors:
            # Color name string passed
            s = re.sub(r'\s+', '', args[0].lower())
            r, g, b, a = colors[s]
        elif len(args) == 1:
            # Otherwise try to convert whatever they passed
            c = convert_to_color(args[0])
            r, g, b, a = c.r, c.g, c.b, c.a
        elif len(args) == 0:
            r, g, b, a = colors['black']
        else:
            raise ValueError("Invalid arguments passed to Color initializer")
        for c in (r, g, b, a):
            if c < 0 or c > 255:
                raise ValueError("r must be in the range [0; 255]")
        self._r = int(r)
        self._g = int(g)
        self._b = int(b)
        self._a = int(a)

    def __copy__(self):
        if self.length == 4:
            return self.r, self.g, self.b, self.a
        if self.length == 3:
            return self.r, self.g, self.b
        if self.length == 2:
            return self.r, self.g
        if self.length == 1:
            return self.r

    # def __hash__(self):
    # return self.__index__()

    def __iter__(self):
        yield self.r
        if self.length > 1:
            yield self.g
        if self.length > 2:
            yield self.b
        if self.length > 3:
            yield self.a

    def __len__(self):
        return self.length

    def __reversed__(self):
        if self.length == 4:
            yield self.a
            yield self.b
            yield self.g
            yield self.r
        elif self.length == 3:
            yield self.b
            yield self.g
            yield self.r
        elif self.length == 2:
            yield self.g
            yield self.r
        elif self.length == 1:
            yield self.r

    def __repr__(self):
        return "({0}, {1}, {2}, {3})".format(self.r, self.g, self.b, self.a)

    def __str__(self):
        return "Color(r={0}, g={1}, b={2}, a={3})".format(
            self.r, self.g, self.b, self.a)

    def __eq__(self, color):
        if isinstance(color, (tuple, Color, Color)):
            return self.r == color[0] and self.g == color[1] and \
                   self.b == color[2] and self.a == color[3]
        else:
            return False

    def __ne__(self, color):
        if isinstance(color, (tuple, Color, Color)):
            return self.r != color[0] or self.g != color[1] or \
                   self.b != color[2] or self.a != color[3]
        else:
            return True

    def __int__(self):
        return self.r << 24 | self.g << 16 | self.b << 8 | self.a

    def __float__(self):
        return (self.r << 24 | self.g << 16 | self.b << 8 | self.a) * 1.0

    def __index__(self):
        return self.r << 24 | self.g << 16 | self.b << 8 | self.a

    def __invert__(self):
        vals = 255 - self.r, 255 - self.g, 255 - self.b, 255 - self.a
        return Color(vals[0], vals[1], vals[2], vals[3])

    def __mod__(self, color):
        vals = (self.r % color.r, self.g % color.g, self.b % color.b,
                self.a % color.a)
        return Color(vals[0], vals[1], vals[2], vals[3])

    def __truediv__(self, color):
        vals = [self.r, self.g, self.b, self.a]
        if color.r != 0:
            vals[0] = self.r / color.r
        if color.g != 0:
            vals[1] = self.g / color.g
        if color.b != 0:
            vals[2] = self.b / color.b
        if color.a != 0:
            vals[3] = self.a / color.a
        return Color(vals[0], vals[1], vals[2], vals[3])

    def __mul__(self, color):
        vals = (min(self.r * color.r, 255), min(self.g * color.g, 255),
                min(self.b * color.b, 255), min(self.a * color.a, 255))
        return Color(vals[0], vals[1], vals[2], vals[3])

    def __sub__(self, color):
        vals = (max(self.r - color.r, 0), max(self.g - color.g, 0),
                max(self.b - color.b, 0), max(self.a - color.a, 0))
        return Color(vals[0], vals[1], vals[2], vals[3])

    def __add__(self, color):
        vals = (min(self.r + color.r, 255), min(self.g + color.g, 255),
                min(self.b + color.b, 255), min(self.a + color.a, 255))
        return Color(vals[0], vals[1], vals[2], vals[3])

    def __getitem__(self, index):
        return (self.r, self.g, self.b, self.a)[index]

    def __setitem__(self, index, val):
        tmp = [self.r, self.g, self.b, self.a]
        tmp[index] = val
        self.r = tmp[0]
        self.g = tmp[1]
        self.b = tmp[2]
        self.a = tmp[3]

    def __floordiv__(self, color):
        vals = [self.r, self.g, self.b, self.a]
        if color.r != 0:
            vals[0] = self.r // color.r
        if color.g != 0:
            vals[1] = self.g // color.g
        if color.b != 0:
            vals[2] = self.b // color.b
        if color.a != 0:
            vals[3] = self.a // color.a
        return Color(vals[0], vals[1], vals[2], vals[3])

    @property
    def length(self):
        """The default Color length is 4. Colors can have lengths 1,2,3 or 4.
        This is useful if you want to unpack to r,g,b and not r,g,b,a. If you
        want to get the length of a Color do len(acolor)."""
        return self._length

    @length.setter
    def length(self, val):
        """The default Color length is 4. Colors can have lengths 1,2,3 or 4.
        This is useful if you want to unpack to r,g,b and not r,g,b,a. If you
        want to get the length of a Color do len(acolor)."""
        if type(val) not in (int, long) or val < 1 or val > 4:
            raise ValueError("Length must be from 1 to 4")
        self._length = val

    @property
    def r(self):
        """Gets or sets the red value of the Color.
        ::

            r -> int"""
        return self._r

    @r.setter
    def r(self, val):
        """Gets or sets the red value of the Color.
        ::

            r -> int"""
        if type(val) not in (int, long):
            raise TypeError("value must be an int")
        if val < 0 or val > 255:
            raise ValueError("The value must be in the range [0; 255]")
        self._r = val

    @property
    def g(self):
        """Gets or sets the green value of the Color.
        ::

            g -> int"""
        return self._g

    @g.setter
    def g(self, val):
        """Gets or sets the green value of the Color.
        ::

            g -> int"""
        if type(val) not in (int, long):
            raise TypeError("value must be an int")
        if val < 0 or val > 255:
            raise ValueError("The value must be in the range [0; 255]")
        self._g = val

    @property
    def b(self):
        """Gets or sets the blue value of the Color.
        ::

            b -> int"""
        return self._b

    @b.setter
    def b(self, val):
        """Gets or sets the blue value of the Color.
        ::

            b -> int"""
        if type(val) not in (int, long):
            raise TypeError("value must be an int")
        if val < 0 or val > 255:
            raise ValueError("The value must be in the range [0; 255]")
        self._b = val

    @property
    def a(self):
        """Gets or sets the alpha value of the Color.
        ::

            a -> int"""
        return self._a

    @a.setter
    def a(self, val):
        """Gets or sets the alpha value of the Color.
        ::

            a -> int"""
        if type(val) not in (int, long):
            raise TypeError("value must be an int")
        if val < 0 or val > 255:
            raise ValueError("The value must be in the range [0; 255]")
        self._a = val

    @property
    def hsva(self):
        """The Color as HSVA value.
        ::

            hsva -> tuple

        The HSVA representation of the Color. The HSVA components are in the
        ranges H = [0, 360], S = [0, 100], V = [0, 100], A = [0, 100]. Note that
        this will not return the absolutely exact HSV values for the set RGB
        values in all cases. Due to the RGB mapping from 0-255 and the HSV
        mapping from 0-100 and 0-360 rounding errors may cause the HSV values to
        differ slightly from what you might expect."""
        rn = self.r / 255.0
        gn = self.g / 255.0
        bn = self.b / 255.0
        an = self.a / 255.0

        maxv = max(rn, gn, bn)
        minv = min(rn, gn, bn)
        diff = maxv - minv

        h = 0
        s = 0
        v = maxv * 100.0
        a = an * 100.0

        if maxv == minv:
            return (h, s, v, a)
        s = 100.0 * (maxv - minv) / maxv

        if maxv == rn:
            h = (60 * (gn - bn) / diff) % 360.0
        elif maxv == gn:
            h = (60 * (bn - rn) / diff) + 120.0
        else:
            h = (60 * (rn - gn) / diff) + 240.0
        if h < 0:
            h += 360.0
        return (h, s, v, a)

    @hsva.setter
    def hsva(self, value):
        """The Color as HSVA value.
        ::

            hsva -> tuple

        The HSVA representation of the Color. The HSVA components are in the
        ranges H = [0, 360], S = [0, 100], V = [0, 100], A = [0, 100]. Note that
        this will not return the absolutely exact HSV values for the set RGB
        values in all cases. Due to the RGB mapping from 0-255 and the HSV
        mapping from 0-100 and 0-360 rounding errors may cause the HSV values to
        differ slightly from what you might expect."""
        h, s, v, a = value
        for x in (h, s, v, a):
            if type(x) not in (int, long, float):
                raise TypeError("HSVA values must be of type float")
        if not (0 <= s <= 100) or not (0 <= v <= 100) or \
                not (0 <= a <= 100) or not (0 <= h <= 360):
            raise ValueError("invalid HSVA value")

        self.a = int((a / 100.0) * 255)
        s /= 100.0
        v /= 100.0

        hi = int(floor(h / 60.0))
        f = (h / 60.0) - hi
        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))
        if hi == 0:
            self.r = int(v * 255)
            self.g = int(t * 255)
            self.b = int(p * 255)
        elif hi == 1:
            self.r = int(q * 255)
            self.g = int(v * 255)
            self.b = int(p * 255)
        elif hi == 2:
            self.r = int(p * 255)
            self.g = int(v * 255)
            self.b = int(t * 255)
        elif hi == 3:
            self.r = int(p * 255)
            self.g = int(q * 255)
            self.b = int(v * 255)
        elif hi == 4:
            self.r = int(t * 255)
            self.g = int(p * 255)
            self.b = int(v * 255)
        elif hi == 5:
            self.r = int(v * 255)
            self.g = int(p * 255)
            self.b = int(q * 255)
        else:
            raise ValueError("invalid HSVA value")

    @property
    def hsla(self):
        """Gets or sets the HSLA representation of the Color.
        ::

            hsla -> tuple

        The HSLA representation of the Color. The HSLA components are in the
        ranges H = [0, 360], S = [0, 100], V = [0, 100], A = [0, 100]. Note that
        this will not return the absolutely exact HSL values for the set RGB
        values in all cases. Due to the RGB mapping from 0-255 and the HSL
        mapping from 0-100 and 0-360 rounding errors may cause the HSL values to
        differ slightly from what you might expect."""
        rn = self.r / 255.0
        gn = self.g / 255.0
        bn = self.b / 255.0
        an = self.a / 255.0

        maxv = max(rn, gn, bn)
        minv = min(rn, gn, bn)
        diff = maxv - minv

        h = 0
        s = 0
        l = 50.0 * (maxv + minv)
        a = an * 100.0

        if maxv == minv:
            return (h, s, l, a)

        if l <= 50.0:
            s = diff / (maxv + minv) * 100.0
        else:
            s = diff / (2.0 - maxv - minv) * 100.0

        if maxv == rn:
            h = (60 * (gn - bn) / diff) % 360.0
        elif maxv == gn:
            h = (60 * (bn - rn) / diff) + 120.0
        else:
            h = (60 * (rn - gn) / diff) + 240.0
        if h < 0:
            h += 360.0
        return (h, s, l, a)

    @hsla.setter
    def hsla(self, value):
        """Gets or sets the HSLA representation of the Color.
        ::

            hsla -> tuple

        The HSLA representation of the Color. The HSLA components are in the
        ranges H = [0, 360], S = [0, 100], V = [0, 100], A = [0, 100]. Note that
        this will not return the absolutely exact HSL values for the set RGB
        values in all cases. Due to the RGB mapping from 0-255 and the HSL
        mapping from 0-100 and 0-360 rounding errors may cause the HSL values to
        differ slightly from what you might expect."""
        h, s, l, a = value
        for x in (h, s, l, a):
            if type(x) not in (int, long, float):
                raise TypeError("HSLA values must be of type float")
        if not (0 <= s <= 100) or not (0 <= l <= 100) or \
                not (0 <= a <= 100) or not (0 <= h <= 360):
            raise ValueError("invalid HSLA value")

        self.a = int((a / 100.0) * 255)

        s /= 100.0
        l /= 100.0

        if s == 0:
            self.r = int(l * 255)
            self.g = int(l * 255)
            self.b = int(l * 255)
            return

        q = 0
        if l < 0.5:
            q = l * (1 + s)
        else:
            q = l + s - (l * s)
        p = 2 * l - q

        ht = h / 360.0

        # r
        h = ht + (1.0 / 3.0)
        if h < 0:
            h += 1
        elif h > 1:
            h -= 1

        if h < (1.0 / 6.0):
            self.r = int((p + ((q - p) * 6 * h)) * 255)
        elif h < 0.5:
            self.r = int(q * 255)
        elif h < (2.0 / 3.0):
            self.r = int((p + ((q - p) * 6 * (2.0 / 3.0 - h))) * 255)
        else:
            self.r = int(p * 255)

        # g
        h = ht
        if h < 0:
            h += 1
        elif h > 1:
            h -= 1

        if h < (1.0 / 6.0):
            self.g = int((p + ((q - p) * 6 * h)) * 255)
        elif h < 0.5:
            self.g = int(q * 255)
        elif h < (2.0 / 3.0):
            self.g = int((p + ((q - p) * 6 * (2.0 / 3.0 - h))) * 255)
        else:
            self.g = int(p * 255)

        # b
        h = ht - (1.0 / 3.0)
        if h < 0:
            h += 1
        elif h > 1:
            h -= 1

        if h < (1.0 / 6.0):
            self.b = int((p + ((q - p) * 6 * h)) * 255)
        elif h < 0.5:
            self.b = int(q * 255)
        elif h < (2.0 / 3.0):
            self.b = int((p + ((q - p) * 6 * (2.0 / 3.0 - h))) * 255)
        else:
            self.b = int(p * 255)

    @property
    def i1i2i3(self):
        """Gets or sets the I1I2I3 representation of the Color.
        ::

            i1i2i3 -> tuple

        The I1I2I3 representation of the Color. The I1I2I3 components are in the
        ranges I1 = [0, 1], I2 = [-0.5, 0.5], I3 = [-0.5, 0.5]. Note that this
        will not return the absolutely exact I1I2I3 values for the set RGB
        values in all cases. Due to the RGB mapping from 0-255 and the I1I2I3
        mapping from 0-1 rounding errors may cause the I1I2I3 values to differ
        slightly from what you might expect."""
        rn = self.r / 255.0
        gn = self.g / 255.0
        bn = self.b / 255.0

        i1 = (rn + gn + bn) / 3.0
        i2 = (rn - bn) / 2.0
        i3 = (2 * gn - rn - bn) / 4.0

        return (i1, i2, i3)

    @i1i2i3.setter
    def i1i2i3(self, value):
        """Gets or sets the I1I2I3 representation of the Color.
        ::

            i1i2i3 -> tuple

        The I1I2I3 representation of the Color. The I1I2I3 components are in the
        ranges I1 = [0, 1], I2 = [-0.5, 0.5], I3 = [-0.5, 0.5]. Note that this
        will not return the absolutely exact I1I2I3 values for the set RGB
        values in all cases. Due to the RGB mapping from 0-255 and the I1I2I3
        mapping from 0-1 rounding errors may cause the I1I2I3 values to differ
        slightly from what you might expect."""
        i1, i2, i3 = value
        for x in (i1, i2, i3):
            if type(x) not in (int, long, float):
                raise TypeError("I1I2I3 values must be of type float")
        if not (0 <= i1 <= 1) or not (-0.5 <= i2 <= 0.5) or \
                not (-0.5 <= i3 <= 0.5):
            raise ValueError("invalid I1I2I3 value")

        ab = i1 - i2 - 2 * i3 / 3.0
        ar = 2 * i2 + ab
        ag = 3 * i1 - ar - ab

        self.r = int(ar * 255)
        self.g = int(ag * 255)
        self.b = int(ab * 255)

    @property
    def cmy(self):
        """Gets or sets the CMY representation of the Color.
        ::

            cmy -> tuple

        The CMY representation of the Color. The CMY components are in the
        ranges C = [0, 1], M = [0, 1], Y = [0, 1]. Note that this will not
        return the absolutely exact CMY values for the set RGB values in all
        cases. Due to the RGB mapping from 0-255 and the CMY mapping from 0-1
        rounding errors may cause the CMY values to differ slightly from what
        you might expect."""
        return (1.0 - self.r / 255.0,
                1.0 - self.g / 255.0,
                1.0 - self.b / 255.0)

    @cmy.setter
    def cmy(self, value):
        """Gets or sets the CMY representation of the Color.
        ::

            cmy -> tuple

        The CMY representation of the Color. The CMY components are in the
        ranges C = [0, 1], M = [0, 1], Y = [0, 1]. Note that this will not
        return the absolutely exact CMY values for the set RGB values in all
        cases. Due to the RGB mapping from 0-255 and the CMY mapping from 0-1
        rounding errors may cause the CMY values to differ slightly from what
        you might expect."""
        c, m, y = value
        if (c < 0 or c > 1) or (m < 0 or m > 1) or (y < 0 or y > 1):
            raise ValueError("invalid CMY value")
        self.r = int((1.0 - c) * 255)
        self.g = int((1.0 - m) * 255)
        self.b = int((1.0 - y) * 255)

    def normalize(self):
        """Returns the RGBA values in a normalized form with the range
        [0;1] as tuple.
        ::

            normalize() -> tuple
        """
        return (self.r / 255.0, self.g / 255.0, self.b / 255.0, self.a / 255.0)

    def correct_gamma(self, gamma):
        """Applies a certain gamma value to the Color.
        ::

            correct_gamma (gamma) -> Color

        Applies a certain gamma value to the Color and returns a new Color with
        the adjusted RGBA values."""

        def decode(color):
            return gamma_decode(color, gamma)

        colors = list(map(decode, [self.r, self.g, self.b, self.a]))

        return Color(colors)

    def set_length(self, length):
        """The default Color length is 4. Colors can have lengths 1,2,3 or 4.
        This is useful if you want to unpack to r,g,b and not r,g,b,a. If you
        want to get the length of a Color do len(acolor).

        This method is just a pygame1 compatibility function.

        acolor.length = 4 is equivalent to acolor.set_length(4)"""
        self.length = length


def gamma_decode(color, gamma):
    corrected = round(255 * pow(color / 255, gamma))
    return max(min(int(corrected), 255), 0)


def is_rgb_color(v):
    """Checks, if the passed value is an item that could be converted to
    a RGB color.
    """
    try:
        if hasattr(v, "r") and hasattr(v, "g") and hasattr(v, "b"):
            if 0 <= int(v.r) <= 255 and 0 <= int(v.g) <= 255 and \
                                    0 <= v.b <= 255:
                return True

        if len(v) >= 3:
            if 0 <= int(v[0]) <= 255 and 0 <= int(v[1]) <= 255 and \
                                    0 < int(v[2]) < 255:
                return True
        return False
    except (TypeError, ValueError):
        return False


def is_rgba_color(v):
    """Checks, if the passed value is an item that could be converted to
    a RGBA color."""
    rgb = is_rgb_color(v)
    if not rgb:
        return False

    try:
        if hasattr(v, "a") and 0 <= int(v.a) <= 255:
            return True
        if len(v) >= 4 and 0 <= int(v[3]) <= 255:
            return True
        return False
    except (TypeError, ValueError):
        return False


def argb_to_color(v):
    """Converts an integer value to a Color, assuming the integer
    represents a 32-bit ARGB value."""
    v = long(v)

    a = ((v & 0xFF000000) >> 24)
    r = ((v & 0x00FF0000) >> 16)
    g = ((v & 0x0000FF00) >> 8)
    b = (v & 0x000000FF)
    return Color(r, g, b, a)


def rgba_to_color(v):
    """Converts an integer value to a Color, assuming the integer
    represents a 32-bit RGBA value."""
    v = long(v)

    r = ((v & 0xFF000000) >> 24)
    g = ((v & 0x00FF0000) >> 16)
    b = ((v & 0x0000FF00) >> 8)
    a = (v & 0x000000FF)
    return Color(r, g, b, a)


def string_to_color(s):
    """Converts a hex color string or color name to a Color value.

    Supported hex values are:

    #RGB
    #RGBA
    #RRGGBB
    #RRGGBBAA

    0xRGB
    0xRGBA
    0xRRGGBB
    0xRRGGBBAA"""
    if type(s) is not str:
        raise TypeError("s must be a string")

    if not (s.startswith("#") or s.startswith("0x")):
        raise ValueError("value is not Color-compatible")

    if s.startswith("#"):
        s = s[1:]
    else:
        s = s[2:]

    r, g, b, a = 255, 255, 255, 255
    if len(s) in (3, 4):
        # A triple/quadruple in the form #ead == #eeaadd
        r = int(s[0], 16) << 4 | int(s[0], 16)
        g = int(s[1], 16) << 4 | int(s[1], 16)
        b = int(s[2], 16) << 4 | int(s[2], 16)
        if len(s) == 4:
            a = int(s[3], 16) << 4 | int(s[3], 16)
    elif len(s) in (6, 8):
        r = int(s[0], 16) << 4 | int(s[1], 16)
        g = int(s[2], 16) << 4 | int(s[3], 16)
        b = int(s[4], 16) << 4 | int(s[5], 16)
        if len(s) == 8:
            a = int(s[6], 16) << 4 | int(s[7], 16)
    else:
        raise ValueError("value is not Color-compatible")
    return Color(r, g, b, a)


def convert_to_color(v):
    """Tries to convert the passed value to a Color object.

    If the color is an integer value, it is assumed to be in ARGB layout."""
    if isinstance(v, Color):
        return v

    if type(v) is str:
        return string_to_color(v)
    if type(v) in (int, long):
        return argb_to_color(v)

    r, g, b, a = 0, 0, 0, 0
    if hasattr(v, "r") and hasattr(v, "g") and hasattr(v, "b"):
        if 0 <= int(v.r) <= 255 and 0 <= int(v.g) <= 255 and \
                                0 <= v.b <= 255:
            r = int(v.r)
            g = int(v.g)
            b = int(v.b)
            if hasattr(v, "a") and 0 <= int(v.a) <= 255:
                a = int(v.a)
        else:
            raise ValueError("value is not Color-compatible")
        return Color(r, g, b, a)

    try:
        length = len(v)
    except:
        raise ValueError("value is not Color-compatible")
    if length < 3:
        raise ValueError("value is not Color-compatible")
    if 0 <= int(v[0]) <= 255 and 0 <= int(v[1]) <= 255 and \
                            0 <= int(v[2]) <= 255:
        r = int(v[0])
        g = int(v[1])
        b = int(v[2])
        if length >= 4 and 0 <= int(v[3]) <= 255:
            a = int(v[3])
        return Color(r, g, b, a)

    raise ValueError("value is not Color-compatible")
