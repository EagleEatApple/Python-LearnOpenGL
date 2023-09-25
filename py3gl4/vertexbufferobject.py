from OpenGL.GL import *
from numpy import ndarray, empty, uint32


class VertexBufferObject:
    def __init__(self, data: ndarray, flags: int = GL_DYNAMIC_STORAGE_BIT) -> None:
        vbo = empty(1, uint32)
        glCreateBuffers(1, vbo)
        self.vbo_id = vbo[0]
        glNamedBufferStorage(self.vbo_id, data.nbytes, data, flags)

    def delete(self) -> None:
        if glIsBuffer(self.vbo_id):
            glDeleteBuffers(1, self.vbo_id)

