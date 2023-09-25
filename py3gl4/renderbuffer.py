from OpenGL.GL import *
from numpy import ndarray, empty, uint32


class Renderbuffer:
    def __init__(self, internal_format: int, width: int, height: int) -> None:
        rbo = empty(1, uint32)
        glCreateRenderbuffers(1, rbo)
        self.rbo_id = rbo[0]
        self.internal_format = internal_format
        self.width = width
        self.height = height
        glNamedRenderbufferStorage(self.rbo_id, internal_format, width, height)

    def bind(self) -> None:
        glBindRenderbuffer(GL_RENDERBUFFER, self.rbo_id)

    def setStorage(self, internal_format, width, height)->None:
        self.internal_format = internal_format
        self.width = width
        self.height = height
        glNamedRenderbufferStorage(self.rbo_id, internal_format, width, height)

    def delete(self) -> None:
        if glIsRenderbuffer(self.rbo_id):
            glDeleteRenderbuffers(1, self.rbo_id)

class RenderbufferMultisample:
    def __init__(self, samples: int, internal_format: int, width: int, height: int) -> None:
        rbo = empty(1, uint32)
        glCreateRenderbuffers(1, rbo)
        self.rbo_id = rbo[0]
        self.samples = samples
        self.internal_format = internal_format
        self.width = width
        self.height = height
        glNamedRenderbufferStorageMultisample(self.rbo_id, samples, internal_format, width, height)

    def delete(self) -> None:
        if glIsRenderbuffer(self.rbo_id):
            glDeleteRenderbuffers(1, self.rbo_id)