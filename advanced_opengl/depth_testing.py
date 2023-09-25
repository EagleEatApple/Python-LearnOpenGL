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

class DepthTesting(CameraWindow):


    def init(self) -> None:
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)
        # always pass the depth test (same effect as glDisable(GL_DEPTH_TEST))
        glDepthFunc(GL_LESS)

        # build and compile shaders
        # ------------------------------------
        self.shader = ProgramVF("shaders/4/1.1.depth_testing.vs",
                                "shaders/4/1.1.depth_testing.fs")

        # set up vertex data (and buffer(s)) and configure vertex attributes
        # ------------------------------------------------------------------
        self.cubeVertices = np.array([
            # positions       texture coords
            -0.5, -0.5, -0.5,  0.0, 0.0,
            0.5, -0.5, -0.5,  1.0, 0.0,
            0.5,  0.5, -0.5,  1.0, 1.0,
            0.5,  0.5, -0.5,  1.0, 1.0,
            -0.5,  0.5, -0.5,  0.0, 1.0,
            -0.5, -0.5, -0.5,  0.0, 0.0,

            -0.5, -0.5,  0.5,  0.0, 0.0,
            0.5, -0.5,  0.5,  1.0, 0.0,
            0.5,  0.5,  0.5,  1.0, 1.0,
            0.5,  0.5,  0.5,  1.0, 1.0,
            -0.5,  0.5,  0.5,  0.0, 1.0,
            -0.5, -0.5,  0.5,  0.0, 0.0,

            -0.5,  0.5,  0.5,  1.0, 0.0,
            -0.5,  0.5, -0.5,  1.0, 1.0,
            -0.5, -0.5, -0.5,  0.0, 1.0,
            -0.5, -0.5, -0.5,  0.0, 1.0,
            -0.5, -0.5,  0.5,  0.0, 0.0,
            -0.5,  0.5,  0.5,  1.0, 0.0,

            0.5,  0.5,  0.5,  1.0, 0.0,
            0.5,  0.5, -0.5,  1.0, 1.0,
            0.5, -0.5, -0.5,  0.0, 1.0,
            0.5, -0.5, -0.5,  0.0, 1.0,
            0.5, -0.5,  0.5,  0.0, 0.0,
            0.5,  0.5,  0.5,  1.0, 0.0,

            -0.5, -0.5, -0.5,  0.0, 1.0,
            0.5, -0.5, -0.5,  1.0, 1.0,
            0.5, -0.5,  0.5,  1.0, 0.0,
            0.5, -0.5,  0.5,  1.0, 0.0,
            -0.5, -0.5,  0.5,  0.0, 0.0,
            -0.5, -0.5, -0.5,  0.0, 1.0,

            -0.5,  0.5, -0.5,  0.0, 1.0,
            0.5,  0.5, -0.5,  1.0, 1.0,
            0.5,  0.5,  0.5,  1.0, 0.0,
            0.5,  0.5,  0.5,  1.0, 0.0,
            -0.5,  0.5,  0.5,  0.0, 0.0,
            -0.5,  0.5, -0.5,  0.0, 1.0
        ], dtype=GLfloat)
        self.planeVertices = np.array([
           # positions       texture coords
            5.0, -0.5,  5.0,  2.0, 0.0,
            -5.0, -0.5,  5.0,  0.0, 0.0,
            -5.0, -0.5, -5.0,  0.0, 2.0,

            5.0, -0.5,  5.0,  2.0, 0.0,
            -5.0, -0.5, -5.0,  0.0, 2.0,
            5.0, -0.5, -5.0,  2.0, 2.0
        ], dtype=GLfloat)

        # vertex attributes
        attribute_aPos = VertexAttribute("aPos", 0, 3, GL_FLOAT, GL_FALSE, 0)
        attribute_aTexCoord = VertexAttribute(
            "aTexCoords", 1, 2, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat))
        # cube VAO
        self.cubeVAO = VertexArrayObject()
        self.cubeVBO = VertexBufferObject(self.cubeVertices)
        self.cubeVAO.setVertexBuffer(self.cubeVBO, 0, 0, 5 * sizeof(GLfloat))
        self.cubeVAO.setVertexAttribute(0, attribute_aPos)
        self.cubeVAO.setVertexAttribute(0, attribute_aTexCoord)
        # plane VAO
        self.planeVAO = VertexArrayObject()
        self.planeVBO = VertexBufferObject(self.planeVertices)
        self.planeVAO.setVertexBuffer(self.planeVBO, 0, 0, 5 * sizeof(GLfloat))
        self.planeVAO.setVertexAttribute(0, attribute_aPos)
        self.planeVAO.setVertexAttribute(0, attribute_aTexCoord)

        # load textures
        self.cubeTexture = ImageTexture2D("textures/marble.jpg")
        self.floorTexture = ImageTexture2D("textures/metal.png")

        # shader configuration
        # ---------------------
        self.shader.use()
        self.shader.setUniform1i("texture1", 0)

    def cleanup(self) -> None:
        self.cubeVAO.delete()
        self.cubeVBO.delete()
        self.planeVAO.delete()
        self.planeVBO.delete()
        self.cubeTexture.delete()
        self.floorTexture.delete()
        self.shader.delete()

    def render(self) -> None:
        super().render()
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.shader.use()
        model = glm.mat4(1.0)
        view = self.camera.GetViewMatrix()
        projection = glm.perspective(
            glm.radians(self.camera.zoom), float(self.width/self.height), 0.1, 100.0)
        self.shader.setUniformMatrix4fv("view", view)
        self.shader.setUniformMatrix4fv("projection",projection)
        # cubes
        self.cubeVAO.bind()
        self.cubeTexture.bind(0)
        model = glm.translate(model, glm.vec3(-1.0, 0.0, -1.0))
        self.shader.setUniformMatrix4fv("model", model)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(2.0, 0.0, 0.0))
        self.shader.setUniformMatrix4fv("model", model)
        glDrawArrays(GL_TRIANGLES, 0, 36)

        # floor
        self.planeVAO.bind()
        self.floorTexture.bind(0)
        model = glm.mat4(1.0)
        self.shader.setUniformMatrix4fv("model", model)
        glDrawArrays(GL_TRIANGLES, 0, 6)

 
if __name__ == "__main__":
    app = App()
    win = DepthTesting(title="Hello, Depth tesing!")
    app.run(win)