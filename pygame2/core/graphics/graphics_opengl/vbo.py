from OpenGL.GL import glDeleteBuffers, glBindBuffer, glBufferData, glGenBuffers

__all__ = ('VertexBufferObject', )


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
