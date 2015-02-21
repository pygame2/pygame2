from __future__ import (print_function, division, absolute_import)

from .corearb import *
from .managed import *
from .internal import GLError


# support for EXT_texture_filter_anisotropic
# see http://www.opengl.org/registry/specs/EXT/texture_filter_anisotropic.txt
GL_TEXTURE_MAX_ANISOTROPY_EXT = 0x84FE
GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT = 0x84FF
