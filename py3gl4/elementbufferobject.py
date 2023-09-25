from OpenGL.GL import *
from numpy import ndarray, empty, uint32


class ElementBufferObject:
    def __init__(self, data: ndarray, flags: int = GL_DYNAMIC_STORAGE_BIT) -> None:
        ebo = empty(1, uint32)
        glCreateBuffers(1, ebo)
        self.ebo_id = ebo[0]
        glNamedBufferStorage(self.ebo_id, data.nbytes, data, flags)
            
    def delete(self) -> None:
        if glIsBuffer(self.ebo_id):
            glDeleteBuffers(1, self.ebo_id)

