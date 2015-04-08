"""
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
import os
import platform

import numpy
import pygame2

from OpenGL.GL import *
from OpenGL.GL.ARB import *

from .texture import Texture


__all__ = [
    'VertexArrayObject',
    'VertexBufferObject',
    'Texture',
    'create_program',
    'get_opengl_version',
    'generate_tex_coords']


def generate_tex_coords():
    """ Generate a VBO that describes texture coordinates.

    This VBO shouldn't need to be changed.  Automatically flips images.

    :return: VBO
    """
    quad_texcoords = numpy.array([
        0.0, 0.0,
        1.0, 0.0,
        0.0, 1.0,
        1.0, 1.0,
    ], dtype='float32')

    vbo = VertexBufferObject(quad_texcoords, GL_ARRAY_BUFFER, GL_STATIC_DRAW)
    return vbo


# TODO: move into gl.info?
def get_opengl_version():
    return glGetInteger(GL_MAJOR_VERSION), glGetInteger(GL_MINOR_VERSION)


def upload_shader(filename, shader_type):
    """Upload shader from file and return shader id
    """
    path = os.path.join(os.path.dirname(pygame2.__file__), 'graphics', filename)
    with open(path) as fp:
        source = fp.read()

    shader_id = glCreateShader(shader_type)
    glShaderSource(shader_id, source)
    glCompileShader(shader_id)

    result = glGetShaderiv(shader_id, GL_COMPILE_STATUS)
    if result == GL_FALSE:
        print('failed', filename)
        info = glGetShaderInfoLog(shader_id)
        print(info)

    return shader_id


def create_program():
    """create program and link shaders
    """
    vtex = upload_shader('vertex_shader.glsl', GL_VERTEX_SHADER)
    frag = upload_shader('fragment_shader.glsl', GL_FRAGMENT_SHADER)

    program_id = glCreateProgram()
    glAttachShader(program_id, vtex)
    glAttachShader(program_id, frag)
    glLinkProgram(program_id)

    result = glGetProgramiv(program_id, GL_LINK_STATUS)
    if result == GL_FALSE:
        print('failed program')
        info = glGetProgramInfoLog(program_id)
        print(info)

    return program_id


class AbstractBuffer:
    """Abstract buffer of byte data.

    :Ivariables:
        `size` : int
            Size of buffer, in bytes
        `ptr` : int
            Memory offset of the buffer, as used by the ``glVertexPointer``
            family of functions
        `target` : int
            OpenGL buffer target, for example ``GL_ARRAY_BUFFER``
        `usage` : int
            OpenGL buffer usage, for example ``GL_DYNAMIC_DRAW``

    """

    def bind(self):
        """Bind this buffer to its OpenGL target."""
        raise NotImplementedError('abstract')

    def unbind(self):
        """Reset the buffer's OpenGL target."""
        raise NotImplementedError('abstract')

    def set_data(self, data):
        """Set the entire contents of the buffer.

        :Parameters:
            `data` : sequence of int or ctypes pointer
                The byte array to set.

        """
        raise NotImplementedError('abstract')

    def set_data_region(self, data, start, length):
        """Set part of the buffer contents.

        :Parameters:
            `data` : sequence of int or ctypes pointer
                The byte array of data to set
            `start` : int
                Offset to start replacing data
            `length` : int
                Length of region to replace

        """
        raise NotImplementedError('abstract')

    def map(self, invalidate=False):
        """Map the entire buffer into system memory.

        The mapped region must be subsequently unmapped with `unmap` before
        performing any other operations on the buffer.

        :Parameters:
            `invalidate` : bool
                If True, the initial contents of the mapped block need not
                reflect the actual contents of the buffer.

        :rtype: ``POINTER(ctypes.c_ubyte)``
        :return: Pointer to the mapped block in memory
        """
        raise NotImplementedError('abstract')

    def unmap(self):
        """Unmap a previously mapped memory block."""
        raise NotImplementedError('abstract')

    def resize(self, size):
        """Resize the buffer to a new size.

        :Parameters:
            `size` : int
                New size of the buffer, in bytes

        """

    def delete(self):
        """Delete this buffer, reducing system resource usage."""
        raise NotImplementedError('abstract')


class AbstractMappable:
    def get_region(self, start, size, ptr_type):
        raise NotImplementedError('abstract')


class VertexArrayObject(AbstractBuffer):
    """WIP"""
    def __init__(self):
        self.id = None
        self.id = glGenVertexArrays(1)

    def __del__(self):
        # id may not be set if binding/generation fails
        if self.id is not None:
            glDeleteVertexArrays(self.id)
            self.id = None

    def bind(self):
        glBindVertexArray(self.id)

    def unbind(self):
        glBindVertexArray(0)


class VertexBufferObject(AbstractBuffer):
    """Lightweight representation of an OpenGL VBO.

    The data in the buffer is not replicated in any system memory (unless it
    is done so by the video driver).  While this can improve memory usage and
    possibly performance, updates to the buffer are relatively slow.

    VBOs are uses for vertexes.
    """

    def __init__(self, data, target, usage):
        self.id = None
        self.target = target
        self.usage = usage
        self.id = glGenBuffers(1)
        self.set_data(data)

    def __del__(self):
        # id may not be set if binding/generation fails
        if self.id is not None:
            glDeleteBuffers(1, [self.id])
            self.id = None

    def bind(self):
        glBindBuffer(self.target, self.id)

    def unbind(self):
        glBindBuffer(self.target, 0)

    def set_data(self, data):
        self.bind()
        glBufferData(self.target, data, self.usage)
        self.unbind()
