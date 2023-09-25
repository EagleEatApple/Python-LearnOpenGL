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


class AdvancedLighting(CameraWindow):


    def init(self) -> None:
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # build and compile shaders
        # ------------------------------------
        self.shader = ProgramVF("shaders/5/1.advanced_lighting.vs",
                                "shaders/5/1.advanced_lighting.fs")

        # set up vertex data (and buffer(s)) and configure vertex attributes
        # ------------------------------------------------------------------

        self.planeVertices = np.array([
            # positions            # normals         # texcoords
            10.0, -0.5,  10.0,  0.0, 1.0, 0.0,  10.0,  0.0,
            -10.0, -0.5,  10.0,  0.0, 1.0, 0.0,   0.0,  0.0,
            -10.0, -0.5, -10.0,  0.0, 1.0, 0.0,   0.0, 10.0,

            10.0, -0.5,  10.0,  0.0, 1.0, 0.0,  10.0,  0.0,
            -10.0, -0.5, -10.0,  0.0, 1.0, 0.0,   0.0, 10.0,
            10.0, -0.5, -10.0,  0.0, 1.0, 0.0,  10.0, 10.0
        ], dtype=GLfloat)

        # vertex attributes
        attribute_aPos = VertexAttribute("aPos", 0, 3, GL_FLOAT, GL_FALSE, 0)
        attribute_aNormal = VertexAttribute("aNormal", 1, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat))
        attribute_aTexCoords = VertexAttribute(
            "aTexCoords", 2, 2, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat))

        # plane VAO
        self.planeVAO = VertexArrayObject()
        self.planeVBO = VertexBufferObject(self.planeVertices)
        self.planeVAO.setVertexBuffer(self.planeVBO, 0, 0, 8 * sizeof(GLfloat))
        self.planeVAO.setVertexAttribute(0, attribute_aPos)
        self.planeVAO.setVertexAttribute(0, attribute_aNormal)
        self.planeVAO.setVertexAttribute(0, attribute_aTexCoords)

        # load textures
        self.floorTexture = ImageTexture2D("textures/wood.png")
        if self.floorTexture.pixel_format == GL_RGBA:
            self.floorTexture.setWrapMode(GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE)
        else:
            self.floorTexture.setWrapMode(GL_REPEAT, GL_REPEAT)
        self.floorTexture.setFiltering(GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR)

        # shader configuration
        # ---------------------
        self.shader.use()
        self.shader.setUniform1i("floorTexture", 0)

        # lighting info
        self.lightPos = glm.vec3(0.0, 0.0, 0.0)
        self.blinn = False
        self.blinnKeyPressed = False

    def cleanup(self) -> None:

        self.planeVAO.delete()
        self.planeVBO.delete()

        self.floorTexture.delete()
        self.shader.delete()

    def render(self) -> None:
        super().render()
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # draw objects
        self.shader.use()
        view = self.camera.GetViewMatrix()
        projection = glm.perspective(
            glm.radians(self.camera.zoom), float(self.width/self.height), 0.1, 100.0)
        self.shader.setUniformMatrix4fv("view", view)
        self.shader.setUniformMatrix4fv("projection",projection)

        # set light uniforms
        self.shader.setUniform3fv("viewPos", self.camera.position)
        self.shader.setUniform3fv("lightPos", self.lightPos)
        self.shader.setUniform1i("blinn", self.blinn)

        # floor
        self.planeVAO.bind()
        self.floorTexture.bind(0)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        print("Blinn-Phong" if self.blinn else "Phong")

    def key_input(self) -> None:
        if glfw.get_key(self.id, glfw.KEY_B) == glfw.PRESS and not self.blinnKeyPressed:
            self.blinn = not self.blinn
            self.blinnKeyPressed = True
        if glfw.get_key(self.id, glfw.KEY_B) == glfw.RELEASE:
            self.blinnKeyPressed = False
        super().key_input()
 
if __name__ == "__main__":
    app = App()
    win = AdvancedLighting(title="Hello, Advanced lighting!")
    app.run(win)