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


class CubemapsSkybox(CameraWindow):


    def init(self) -> None:
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)

        # build and compile shaders
        # ------------------------------------
        self.shader = ProgramVF("shaders/4/6.1.cubemaps.vs",
                                "shaders/4/6.1.cubemaps.fs")

        self.skyboxShader = ProgramVF("shaders/4/6.1.skybox.vs",
                                "shaders/4/6.1.skybox.fs")

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
        self.skyboxVertices = np.array([
            # positions  
            -1.0,  1.0, -1.0,
            -1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            1.0,  1.0, -1.0,
            -1.0,  1.0, -1.0,

            -1.0, -1.0,  1.0,
            -1.0, -1.0, -1.0,
            -1.0,  1.0, -1.0,
            -1.0,  1.0, -1.0,
            -1.0,  1.0,  1.0,
            -1.0, -1.0,  1.0,

            1.0, -1.0, -1.0,
            1.0, -1.0,  1.0,
            1.0,  1.0,  1.0,
            1.0,  1.0,  1.0,
            1.0,  1.0, -1.0,
            1.0, -1.0, -1.0,

            -1.0, -1.0,  1.0,
            -1.0,  1.0,  1.0,
            1.0,  1.0,  1.0,
            1.0,  1.0,  1.0,
            1.0, -1.0,  1.0,
            -1.0, -1.0,  1.0,

            -1.0,  1.0, -1.0,
            1.0,  1.0, -1.0,
            1.0,  1.0,  1.0,
            1.0,  1.0,  1.0,
            -1.0,  1.0,  1.0,
            -1.0,  1.0, -1.0,

            -1.0, -1.0, -1.0,
            -1.0, -1.0,  1.0,
            1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            -1.0, -1.0,  1.0,
            1.0, -1.0,  1.0
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
        # skybox VAO
        skybox_aPos = VertexAttribute("aPos", 0, 3, GL_FLOAT, GL_FALSE, 0)
        self.skyboxVAO = VertexArrayObject()
        self.skyboxVBO = VertexBufferObject(self.skyboxVertices)
        self.skyboxVAO.setVertexBuffer(self.skyboxVBO, 0, 0, 3 * sizeof(GLfloat))
        self.skyboxVAO.setVertexAttribute(0, skybox_aPos)

        # load textures
        self.cubeTexture = ImageTexture2D("textures/container.jpg")
        faces = [
            "textures/skybox/right.jpg", 
            "textures/skybox/left.jpg",
            "textures/skybox/top.jpg",
            "textures/skybox/bottom.jpg",
            "textures/skybox/front.jpg",
            "textures/skybox/back.jpg"
        ]
        self.cubemapTexture = ImageTextureCubemap(faces)

        # shader configuration
        # ---------------------
        self.shader.use()
        self.shader.setUniform1i("texture1", 0)

        self.skyboxShader.use()
        self.skyboxShader.setUniform1i("skybox", 0)

    def cleanup(self) -> None:
        self.cubeVAO.delete()
        self.cubeVBO.delete()
        self.cubeTexture.delete()
        self.shader.delete()

    def render(self) -> None:
        super().render()
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # draw scene as normal
        self.shader.use()
        model = glm.mat4(1.0)
        view = self.camera.GetViewMatrix()
        projection = glm.perspective(
            glm.radians(self.camera.zoom), float(self.width/self.height), 0.1, 100.0)
        self.shader.setUniformMatrix4fv("model", model)
        self.shader.setUniformMatrix4fv("view", view)
        self.shader.setUniformMatrix4fv("projection",projection)
        # cubes
        self.cubeVAO.bind()
        self.cubeTexture.bind(0)
        glDrawArrays(GL_TRIANGLES, 0, 36)


        # draw skybox as last
        glDepthFunc(GL_LEQUAL)
        self.skyboxShader.use()
        view = glm.mat4(glm.mat3(self.camera.GetViewMatrix())) 
        self.skyboxShader.setUniformMatrix4fv("view", view)
        self.skyboxShader.setUniformMatrix4fv("projection",projection)

        # skybox cube
        self.skyboxVAO.bind()
        self.cubemapTexture.bind(0)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        glDepthFunc(GL_LESS)

if __name__ == "__main__":
    app = App()
    win = CubemapsSkybox(title="Hello, Cubemap!")
    app.run(win)

