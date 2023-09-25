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

class GammaCorrection(CameraWindow):


    def init(self) -> None:
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # build and compile shaders
        # ------------------------------------
        self.shader = ProgramVF("shaders/5/2.gamma_correction.vs",
                                "shaders/5/2.gamma_correction.fs")

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
        self.floorTexture.setWrapMode(GL_REPEAT, GL_REPEAT)
        self.floorTexture.setFiltering(GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR)
        self.floorTextureGammaCorrected = ImageTexture2D("textures/wood.png",srgb=True)
        self.floorTextureGammaCorrected.setWrapMode(GL_REPEAT, GL_REPEAT)
        self.floorTextureGammaCorrected.setFiltering(GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR)

        # shader configuration
        # ---------------------
        self.shader.use()
        self.shader.setUniform1i("floorTexture", 0)

        # lighting info
        self.lightPositions = np.array([
            glm.vec3(-3.0, 0.0, 0.0),
            glm.vec3(-1.0, 0.0, 0.0),
            glm.vec3 (1.0, 0.0, 0.0),
            glm.vec3 (3.0, 0.0, 0.0)
        ])

        self.lightColors = np.array([
            glm.vec3(0.25),
            glm.vec3(0.50),
            glm.vec3(0.75),
            glm.vec3(1.00)
        ])
        self.gammaEnabled = False
        self.gammaKeyPressed = False

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
        glUniform3fv(glGetUniformLocation(self.shader.program_id, "lightPositions"), 4, self.lightPositions)
        glUniform3fv(glGetUniformLocation(self.shader.program_id, "lightColors"), 4, self.lightColors)
        self.shader.setUniform3fv("viewPos", self.camera.position)
        self.shader.setUniform1i("gamma", self.gammaEnabled)

        # floor
        self.planeVAO.bind()
        if self.gammaEnabled:
            self.floorTextureGammaCorrected.bind(0)
        else:
            self.floorTexture.bind(0)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        print("Gamma enabled" if self.gammaEnabled else "Gamma disabled")


    def key_input(self) -> None:
        if glfw.get_key(self.id, glfw.KEY_SPACE) == glfw.PRESS and not self.gammaKeyPressed:
            self.gammaEnabled = not self.gammaEnabled
            self.gammaKeyPressed = True
        if glfw.get_key(self.id, glfw.KEY_SPACE) == glfw.RELEASE:
            self.gammaKeyPressed = False
        super().key_input()
 
if __name__ == "__main__":
    app = App()
    win = GammaCorrection(title="Hello, Gamma correction!")
    app.run(win)