import sys
parent_dir = "../Python-LearnOpenGL"
sys.path.append(parent_dir)

from OpenGL.GL import *
import numpy as np

from py3gl4 import *
from app import *

class HelloTriangle(GLWindow):
    def init(self) -> None:
        self.shaderProgram = ProgramVF("shaders/1/2.1.shader.vs", "shaders/1/2.1.shader.fs")

        self.vertices = np.array([
            -0.5,  -0.5, 0.0,  # left
            0.5, -0.5, 0.0,  # right
            0.0,  0.5, 0.0,  # top
        ], dtype=GLFLOAT)
        self.VAO = VertexArrayObject()
        self.VBO = VertexBufferObject(self.vertices)
        attribute_aPos = VertexAttribute("aPos", 0, 3, GL_FLOAT, False, 0)
        self.VAO.setVertexBuffer(self.VBO, 0, 0, 3 * sizeof(GLFLOAT))
        self.VAO.setVertexAttribute(0, attribute_aPos)

    def cleanup(self) -> None:
        self.VAO.delete()
        self.VBO.delete()
        self.shaderProgram.delete()

    def render(self) -> None:
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        self.shaderProgram.use()
        self.VAO.bind()
        glDrawArrays(GL_TRIANGLES, 0, 3)


if __name__ == "__main__":
    app = App()
    win = HelloTriangle(title="Hello, Triangle!")
    app.run(win)