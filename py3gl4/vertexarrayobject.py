from OpenGL.GL import *
from numpy import ndarray, empty, uint32

from py3gl4.vertexbufferobject import VertexBufferObject
from py3gl4.elementbufferobject import ElementBufferObject


class VertexAttribute:
    def __init__(self, name: str, index: int, size: int, type: int, normalized: bool=False, offset: int=0) -> None:
        self.name = name
        self.index = index
        self.size = size
        self.type = type
        self.normalized = normalized
        self.offset = offset


class VertexArrayObject:
    def __init__(self) -> None:
        vao = empty(1, uint32)
        glCreateVertexArrays(1, vao)
        self.vao_id = vao[0]

    def bind(self) -> None:
        glBindVertexArray(self.vao_id)

    def delete(self) -> None:
        if glIsVertexArray(self.vao_id):
            glDeleteVertexArrays(1, self.vao_id)

    def setElementBuffer(self, buffer: ElementBufferObject) -> None:
        glVertexArrayElementBuffer(self.vao_id, buffer.ebo_id)

    def setVertexBuffer(self, buffer: VertexBufferObject, bindingindex: int, offset: int, stride: int) -> None:
        glVertexArrayVertexBuffer(
            self.vao_id, bindingindex, buffer.vbo_id, offset, stride)

    def setVertexAttribute(self, bindingindex: int, attrib: VertexAttribute) -> None:
        glEnableVertexArrayAttrib(self.vao_id, attrib.index)
        glVertexArrayAttribFormat(
            self.vao_id, attrib.index, attrib.size, attrib.type, attrib.normalized, attrib.offset)
        glVertexArrayAttribBinding(self.vao_id, attrib.index, bindingindex)

    def setBindingDivisor(self, bindingindex: int, divisor: int)-> None:
        glVertexArrayBindingDivisor(self.vao_id, bindingindex, divisor)
