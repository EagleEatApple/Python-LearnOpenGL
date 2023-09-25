import sys
parent_dir = "../Python-LearnOpenGL"
sys.path.append(parent_dir)

from OpenGL.GL import *
import numpy as np

from py3gl4 import *
from app import *


class ShadersClass(GLWindow):
    def init(self) -> None:
        # build and compile our shader program
        # ------------------------------------

        self.ourShader = ProgramVF("shaders/1/3.3.shader.vs", "shaders/1/3.3.shader.fs")

        # set up vertex data (and buffer(s)) and configure vertex attributes
        # ------------------------------------------------------------------
        self.vertices = np.array([
            0.5, -0.5, 0.0,  1.0, 0.0, 0.0, # bottom right
           -0.5, -0.5, 0.0,  0.0, 1.0, 0.0,  # bottom left
            0.0,  0.5, 0.0,  0.0, 0.0, 1.0  # top
        ], dtype=GLfloat)

        self.VAO = VertexArrayObject()
        self.VBO = VertexBufferObject(self.vertices)
        
        attribute_aPos = VertexAttribute("aPos", 0, 3, GL_FLOAT, GL_FALSE, 0)
        attribute_aColor = VertexAttribute("aColor", 1, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat))

        self.VAO.setVertexBuffer(self.VBO, 0, 0, 6 * sizeof(GLfloat))
        self.VAO.setVertexAttribute(0, attribute_aPos)
        self.VAO.setVertexAttribute(0, attribute_aColor)


    def cleanup(self) -> None:
        self.VAO.delete()
        self.VBO.delete()
        self.ourShader.delete()

    def render(self) -> None:
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        
        # render the triangle
        self.ourShader.use()
        self.VAO.bind()
        glDrawArrays(GL_TRIANGLES, 0, 3)

if __name__ == "__main__":
    app = App()
    win = ShadersClass(title="Hello, Shader Class!")
    app.run(win)