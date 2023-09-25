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


class Framebuffers(CameraWindow):


    def init(self) -> None:
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)

        # build and compile shaders
        # ------------------------------------
        self.shader = ProgramVF("shaders/4/5.1.framebuffers.vs",
                                "shaders/4/5.1.framebuffers.fs")

        self.screenShader = ProgramVF("shaders/4/5.1.framebuffers_screen.vs",
                                "shaders/4/5.1.framebuffers_screen.fs")

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
        self.quadVertices = np.array([
           # positions   texture coords
            -1.0,  1.0,  0.0, 1.0,
            -1.0, -1.0,  0.0, 0.0,
            1.0, -1.0,  1.0, 0.0,

            -1.0,  1.0,  0.0, 1.0,
            1.0, -1.0,  1.0, 0.0,
            1.0,  1.0,  1.0, 1.0
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
        # screen quad VAO
        quad_aPos = VertexAttribute("aPos", 0, 2, GL_FLOAT, GL_FALSE, 0)
        quad_aTexCoord = VertexAttribute(
            "aTexCoords", 1, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(GLfloat))
        self.quadVAO = VertexArrayObject()
        self.quadVBO = VertexBufferObject(self.quadVertices)
        self.quadVAO.setVertexBuffer(self.quadVBO, 0, 0, 4 * sizeof(GLfloat))
        self.quadVAO.setVertexAttribute(0, quad_aPos)
        self.quadVAO.setVertexAttribute(0, quad_aTexCoord)

        # load textures
        self.cubeTexture = ImageTexture2D("textures/container.jpg")
        self.floorTexture = ImageTexture2D("textures/metal.png")

        # shader configuration
        # ---------------------
        self.shader.use()
        self.shader.setUniform1i("texture1", 0)

        self.screenShader.use()
        self.screenShader.setUniform1i("screenTexture", 0)

        # framebuffer configuration
        self.framebuffer = Framebuffer()
        # create a color attachment texture
        self.textureColorbuffer = Texture2D(1, GL_RGB16F, self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE)
        self.textureColorbuffer.setFiltering(GL_LINEAR, GL_LINEAR)
        self.framebuffer.attachTexture2D(GL_COLOR_ATTACHMENT0, self.textureColorbuffer, 0)
        # create a renderbuffer object for depth and stencil attachment (we won't be sampling these)
        self.rbo = Renderbuffer(GL_DEPTH24_STENCIL8, self.width, self.height)
        self.framebuffer.attachRenderbuffer(GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, self.rbo)
        if self.framebuffer.isComplete() is not True:
            raise RuntimeError('ERROR::FRAMEBUFFER:: Framebuffer is not complete!')

    def cleanup(self) -> None:
        self.cubeVAO.delete()
        self.cubeVBO.delete()
        self.planeVAO.delete()
        self.planeVBO.delete()
        self.quadVAO.delete()
        self.quadVBO.delete()
        self.cubeTexture.delete()
        self.floorTexture.delete()
        self.shader.delete()
        self.screenShader.delete()
        self.framebuffer.delete()
        self.textureColorbuffer.delete()
        self.rbo.delete()

    def render(self) -> None:
        super().render()
        # bind to framebuffer and draw scene as we normally would to color texture 
        self.framebuffer.bind()
        glEnable(GL_DEPTH_TEST)

        # make sure we clear the framebuffer's content
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


        # now bind back to default framebuffer and draw a quad plane with the attached framebuffer color texture
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glDisable(GL_DEPTH_TEST)
        # clear all relevant buffers
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)     

        self.screenShader.use()
        self.quadVAO.bind()
        self.textureColorbuffer.bind(0)
        glDrawArrays(GL_TRIANGLES, 0, 6)

if __name__ == "__main__":
    app = App()
    win = Framebuffers(title="Hello, Framebuffer!")
    app.run(win)
