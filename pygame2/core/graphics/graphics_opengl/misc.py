import os

from OpenGL.GL import *



# TODO: move into gl.info?
def get_opengl_version():
    return glGetInteger(GL_MAJOR_VERSION), glGetInteger(GL_MINOR_VERSION)


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



