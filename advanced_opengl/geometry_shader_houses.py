import sys
parent_dir = "../Python-LearnOpenGL"
sys.path.append(parent_dir)

from math import sin, cos
import random
from OpenGL.GL import *
import numpy as np
import glm
import glfw

from py3gl4 import *
from app import *

class GeometryShaderHouses(GLWindow):


    def init(self) -> None:
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)

        # build and compile shaders
        # ------------------------------------
        self.shader = ProgramVGF("shaders/4/9.1.geometry_shader.vs",
                                "shaders/4/9.1.geometry_shader.gs",
                                "shaders/4/9.1.geometry_shader.fs")



        # set up vertex data (and buffer(s)) and configure vertex attributes
        # ------------------------------------------------------------------
        self.points = np.array([
            -0.5,  0.5, 1.0, 0.0, 0.0, # top-left
            0.5,  0.5, 0.0, 1.0, 0.0, # top-right
            0.5, -0.5, 0.0, 0.0, 1.0, # bottom-right
            -0.5, -0.5, 1.0, 1.0, 0.0 # bottom-left
        ], dtype=GLfloat)


        # vertex attributes
        attribute_aPos = VertexAttribute("aPos", 0, 2, GL_FLOAT, GL_FALSE, 0)
        attribute_aColor = VertexAttribute("aColor", 1, 3, GL_FLOAT, GL_FALSE, 2 * sizeof(GLfloat))
        # cube VAO
        self.VAO = VertexArrayObject()
        self.VBO = VertexBufferObject(self.points)
        self.VAO.setVertexBuffer(self.VBO, 0, 0, 5 * sizeof(GLfloat))
        self.VAO.setVertexAttribute(0, attribute_aPos)
        self.VAO.setVertexAttribute(0, attribute_aColor)

    def cleanup(self) -> None:
        self.VAO.delete()
        self.VBO.delete()


    def render(self) -> None:
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # draw points
        self.shader.use()
        self.VAO.bind()
        glDrawArrays(GL_POINTS, 0, 4)
 
if __name__ == "__main__":
    app = App()
    win = GeometryShaderHouses(title="Hello, Geometry shader!")
    app.run(win)