import sys
parent_dir = "../Python-LearnOpenGL"
sys.path.append(parent_dir)

from OpenGL.GL import *
import numpy as np

from py3gl4 import *
from app import *


class HelloTriangleIndexed(GLWindow):
    def init(self) -> None:
        self.shaderProgram = ProgramVF("shaders/1/2.2.shader.vs", "shaders/1/2.2.shader.fs")

        self.vertices = np.array([
            0.5,  0.5, 0.0,  # top right
            0.5, -0.5, 0.0,  # bottom right
            -0.5,  -0.5, 0.0,  # bottom left
            -0.5, 0.5, 0.0,  # top left
        ], dtype=GLFLOAT)
        # note that we start from 0!
        self.indices = np.array([
            0, 1, 3, # first Triangle
            1, 2, 3, # second Triangle
        ], dtype=GLuint)
        self.VAO = VertexArrayObject()
        self.VBO = VertexBufferObject(self.vertices)
        self.EBO = ElementBufferObject(self.indices)

        attribute_aPos = VertexAttribute("aPos", 0, 3, GL_FLOAT, False, 0)
        self.VAO.setVertexBuffer(self.VBO, 0, 0, 3 * sizeof(GLFLOAT))
        self.VAO.setVertexAttribute(0, attribute_aPos)
        self.VAO.setElementBuffer(self.EBO)


    def cleanup(self) -> None:
        self.VAO.delete()
        self.VBO.delete()
        self.EBO.delete()
        self.shaderProgram.delete()

    def render(self) -> None:
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        self.shaderProgram.use()
        self.VAO.bind()
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, ctypes.c_void_p(0))

if __name__ == "__main__":
    app = App()
    win = HelloTriangleIndexed(title="Hello, Triangle!")
    app.run(win)