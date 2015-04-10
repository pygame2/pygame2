"""
The end result of this work will be a grpahics system that works
with modular backends.  OpenGL is in development, other will follow
OpenGL is very unstable right now.

For cross platform support, version OpenGL 3.3 will be the lowest
supported version.  Currently, it is the best choice for OS X, and
is supported well on windows and linux.

this module contains basic classes to support opengl.  the pygame2
graphics api exists to remove any direct calling of opengl functions
from our normal framework.

in the future, when other APIs are explored (webgl, vulkan), then it
will only be necessary to change the graphics module.
"""
# declare our graphics provider
from pygame2.core import core_modules

core_modules['graphics'] = ('graphics_pyopengl', )

import OpenGL

OpenGL.ERROR_CHECKING = True

from .renderer import SpriteRenderer
from .sprite import Sprite
from .texture import Texture
