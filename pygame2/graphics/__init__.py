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

    shader must be in pygame2/graphics folder
    """
    path = os.path.join(os.path.dirname(pygame2.__file__), 'graphics', filename)
    with open(path) as fp:
        source = fp.read()

    shader_id = glCreateShader(shader_type)
    glShaderSource(shader_id, source)
    glCompileShader(shader_id)

    result = glGetShaderiv(shader_id, GL_COMPILE_STATUS)
    if result == GL_FALSE:
        print('failed shader compile', filename)
        info = glGetShaderInfoLog(shader_id)
        print(info)

    return shader_id


def create_program(shaders):
    """create program and link shaders

    :param shaders: list, (filename, type) tuples
    """
    program_id = glCreateProgram()
    shaders = (upload_shader(*args) for args in shaders)
    for shader_id in shaders:
        glAttachShader(program_id, shader_id)
    glLinkProgram(program_id)

    result = glGetProgramiv(program_id, GL_LINK_STATUS)
    if result == GL_FALSE:
        print('failed program linking')
        info = glGetProgramInfoLog(program_id)
        print(info)

    return program_id


class VertexArrayObject:
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


class VertexBufferObject:
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
