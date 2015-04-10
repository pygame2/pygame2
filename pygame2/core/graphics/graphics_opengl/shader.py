import os

from OpenGL.GL import *


__all__ = ('upload_shader', )


def upload_shader(filename, shader_type):
    """Upload shader from file and return shader id
    shader must be in the same folder
    """
    path = os.path.join(os.path.dirname(__file__), filename)
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
