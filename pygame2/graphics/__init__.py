"""
OpenGL is very unstable right now.

For cross platform support, version 3.3 will be the lowest supported version.
Currently, it is the best choice for OS X, and is supported well on windows
and linux.
"""
from pygame2.gl import *

__all__ = ('draw', )


def draw(size, mode, *data):
    """Draw a primitive immediately.

    :Parameters:
        `size` : int
            Number of vertices given
        `mode` : gl primitive type
            OpenGL drawing mode, e.g. ``GL_TRIANGLES``,
            avoiding quotes.
        `data` : data items
            Attribute formats and data.  See the module summary for
            details.

    """
    # glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)

    buffers = list()
    for fmt, array in data:
        attribute = vertexattribute.create_attribute(fmt)
        assert size == len(array) // attribute.count, \
            'Data for %s is incorrect length' % fmt
        buffer = vertexbuffer.create_mappable_buffer(
            size * attribute.stride, vbo=False)

        attribute.set_region(buffer, 0, size, array)
        attribute.enable()
        attribute.set_pointer(buffer.ptr)
        buffers.append(buffer)

    glDrawArrays(mode, 0, size)
    glFlush()

    # glPopClientAttrib()
