from OpenGL.GL import *


# TODO: move into gl.info?
def get_opengl_version():
    return glGetInteger(GL_MAJOR_VERSION), glGetInteger(GL_MINOR_VERSION)


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



