import sys
parent_dir = "../Python-LearnOpenGL"
sys.path.append(parent_dir)

from OpenGL.GL import *
import numpy as np

from py3gl4 import *
from app import *


class Textures(GLWindow):
    def init(self) -> None:
        self.ourShader = ProgramVF("shaders/1/4.1.texture.vs", 
                                   "shaders/1/4.1.texture.fs")

        # set up vertex data (and buffer(s)) and configure vertex attributes
        # ------------------------------------------------------------------
        self.vertices = np.array([
            # positions     colors         texture coords
            0.5,  0.5, 0.0,   1.0, 0.0, 0.0,   1.0, 1.0, # top right
            0.5, -0.5, 0.0,   0.0, 1.0, 0.0,   1.0, 0.0,    # bottom right
            -0.5, -0.5, 0.0,   0.0, 0.0, 1.0,   0.0, 0.0,  # bottom left
            -0.5,  0.5, 0.0,   1.0, 1.0, 0.0,   0.0, 1.0   # top
        ], dtype=GLFLOAT)
        self.indices = np.array([
            0, 1, 3,  # first Triangle
            1, 2, 3  # second Triangle
        ], dtype=GLUINT)

        self.VAO = VertexArrayObject()
        self.VBO = VertexBufferObject(self.vertices)
        self.EBO = ElementBufferObject(self.indices)
        attribute_aPos = VertexAttribute("aPos", 0, 3, GL_FLOAT, GL_FALSE, 0)
        attribute_aColor = VertexAttribute("vertexColor", 1, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLFLOAT))
        attribute_aTexCoord = VertexAttribute("aTexCoord", 2, 2, GL_FLOAT, GL_FALSE, 6 * sizeof(GLFLOAT))
        self.VAO.setVertexBuffer(self.VBO, 0, 0, 8 * sizeof(GLFLOAT))
        self.VAO.setVertexAttribute(0, attribute_aPos)
        self.VAO.setVertexAttribute(0, attribute_aColor)
        self.VAO.setVertexAttribute(0, attribute_aTexCoord)
        self.VAO.setElementBuffer(self.EBO)

        # load and create a texture
        self.texture = ImageTexture2D("textures/container.jpg")
        self.texture.setWrapMode(GL_REPEAT, GL_REPEAT)
        self.texture.setFiltering(GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR)

    def cleanup(self) -> None:
        self.VAO.delete()
        self.VBO.delete()
        self.EBO.delete()
        self.texture.delete()
        self.ourShader.delete()

    def render(self) -> None:
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # bind Texture
        self.texture.bind(0)
        
        # render container
        self.ourShader.use()
        self.VAO.bind()
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, ctypes.c_void_p(0))

if __name__ == "__main__":
    app = App()
    win = Textures(title="Hello, Texture!")
    app.run(win)