from OpenGL.GL import *

from .shader import upload_shader

__all__ = ('create_program', )


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
