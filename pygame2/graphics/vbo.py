"""
Vertex Buffer Objects
=====================

incomplete
"""
from pygame2.gl import *

__all__ = ('VBO', 'VertexBatch')


class VBO:
    """
    Vertex Buffer Object
    """
    def __init__(self, vertex_format=None):
        self.vertex_format = vertex_format
        self.usage = None
        self.target = None
        self.id = None

    def delete(self):
        """Forse VBO data to be unloaded
        """
        pass

    def update_buffer(self):
        """Mark that data has changed and let the GPU consume
        new vertex data

        :return: None
        """
        pass

    def bind(self):
        """GL Bind
        """
        self.update_buffer()
        glBindBuffer(GL_ARRAY_BUFFER, self.id)

    def unbind(self):
        """GL unbind
        """
        glBindBuffer(GL_ARRAY_BUFFER, 0)


class VertexBatch:
    def __init__(self, **kwargs):
        self.usage = GL_DYNAMIC_DRAW  # copy/static
        self.mode = GL_TRIANGLES      # points/lines/triangle_fan (quads)
        vbo = kwargs.get('vbo', None)
        # if self.vbo is None:
        #     self.vbo = VBO()
        self.id = 0

    def draw(self):
        # create when needed?
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.id)
        # upload to GPU if needed
        self.vbo.bind()
        count = 0
        NULL = 0
        # glDrawElements(self.mode, count, GL_UNSIGNED_SHORT, NULL)
