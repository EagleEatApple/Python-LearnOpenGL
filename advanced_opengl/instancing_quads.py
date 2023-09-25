import sys
parent_dir = "../Python-LearnOpenGL"
sys.path.append(parent_dir)

from math import sin, cos

from OpenGL.GL import *
import numpy as np
import glm
import glfw

from py3gl4 import *
from app import *



class Instancing_quads(GLWindow):


    def init(self) -> None:
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)

        # build and compile shaders
        # ------------------------------------
        self.shader = ProgramVF("shaders/4/10.1.instancing.vs",
                                "shaders/4/10.1.instancing.fs")

        # generate a list of 100 quad locations/translation-vectors
        # ---------------------------------------------------------
        translations = np.zeros(shape=(100, 2), dtype=np.float32)
        index = 0
        offset = 0.1
        for y in range(-10, 10, 2):
            for x in range(-10, 10, 2):
                translations[index][0]  = x / 10.0 + offset
                translations[index][1] = y / 10.0 + offset
                index += 1

        # store instance data in an array buffer
        self.instanceVBO = VertexBufferObject(translations)

        # set up vertex data (and buffer(s)) and configure vertex attributes
        # ------------------------------------------------------------------
        self.quadVertices = np.array([
            # positions     # colors
            -0.05,  0.05,  1.0, 0.0, 0.0,
            0.05, -0.05,  0.0, 1.0, 0.0,
            -0.05, -0.05,  0.0, 0.0, 1.0,

            -0.05,  0.05,  1.0, 0.0, 0.0,
            0.05, -0.05,  0.0, 1.0, 0.0,
            0.05,  0.05,  0.0, 1.0, 1.0
        ], dtype=GLfloat)

        # vertex attributes
        attribute_aPos = VertexAttribute("aPos", 0, 2, GL_FLOAT, GL_FALSE, 0)
        attribute_aColor = VertexAttribute("aColor", 1, 3, GL_FLOAT, GL_FALSE, 2 * sizeof(GLfloat))
        attribute_aOffset = VertexAttribute("aOffset", 2, 2, GL_FLOAT, GL_FALSE, 0)
        # cube VAO
        self.quadVAO = VertexArrayObject()
        self.quadVBO = VertexBufferObject(self.quadVertices)
        self.quadVAO.setVertexBuffer(self.quadVBO, 0, 0, 5 * sizeof(GLfloat))
        self.quadVAO.setVertexAttribute(0, attribute_aPos)
        self.quadVAO.setVertexAttribute(0, attribute_aColor)
        self.quadVAO.setVertexBuffer(self.instanceVBO, 1, 0, 2 * sizeof(GLfloat))
        self.quadVAO.setVertexAttribute(1, attribute_aOffset)
        # tell OpenGL this is an instanced vertex attribute
        self.quadVAO.setBindingDivisor(1, 1)

    def cleanup(self) -> None:
        self.quadVAO.delete()
        self.quadVBO.delete()
        self.shader.delete()


    def render(self) -> None:
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # draw 100 instanced quads
        self.shader.use()
        self.quadVAO.bind()
        glDrawArraysInstanced(GL_TRIANGLES, 0, 6, 100)


if __name__ == "__main__":
    app = App()
    win = Instancing_quads(title="Hello, Instancing!")
    app.run(win)