from OpenGL.GL import *
from numpy import empty, uint32


class UniformBufferObject:
    def __init__(self, binding_point:int, size:int, usage:int=GL_DYNAMIC_STORAGE_BIT) -> None:
        ubo = empty(1, uint32)
        glCreateBuffers(1, ubo)
        self.ubo_id = ubo[0]
        glNamedBufferStorage(self.ubo_id, size, None, usage)
        glBindBufferRange(GL_UNIFORM_BUFFER, binding_point, self.ubo_id, 0, size)
            
    def delete(self) -> None:
        if glIsBuffer(self.ubo_id):
            glDeleteBuffers(1, self.ubo_id)

    def update(self, offset:int, size:int, data:ctypes.c_void_p) -> None:
        glNamedBufferSubData(self.ubo_id, offset, size, data)
