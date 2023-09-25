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


class AntiAliaxingOffscreen(CameraWindow):


    def init(self) -> None:
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)

        # build and compile shaders
        # ------------------------------------
        self.shader = ProgramVF("shaders/4/11.2.anti_aliasing.vs",
                                "shaders/4/11.2.anti_aliasing.fs")

        self.screenShader = ProgramVF("shaders/4/11.2.aa_post.vs",
                                      "shaders/4/11.2.aa_post.fs")

        # set up vertex data (and buffer(s)) and configure vertex attributes
        # ------------------------------------------------------------------
        self.cubeVertices = np.array([
            # positions
            -0.5, -0.5, -0.5,
            0.5, -0.5, -0.5,
            0.5,  0.5, -0.5,
            0.5,  0.5, -0.5,
            -0.5,  0.5, -0.5,
            -0.5, -0.5, -0.5,

            -0.5, -0.5,  0.5,
            0.5, -0.5,  0.5,
            0.5,  0.5,  0.5,
            0.5,  0.5,  0.5,
            -0.5,  0.5,  0.5,
            -0.5, -0.5,  0.5,

            -0.5,  0.5,  0.5,
            -0.5,  0.5, -0.5,
            -0.5, -0.5, -0.5,
            -0.5, -0.5, -0.5,
            -0.5, -0.5,  0.5,
            -0.5,  0.5,  0.5,

            0.5,  0.5,  0.5,
            0.5,  0.5, -0.5,
            0.5, -0.5, -0.5,
            0.5, -0.5, -0.5,
            0.5, -0.5,  0.5,
            0.5,  0.5,  0.5,

            -0.5, -0.5, -0.5,
            0.5, -0.5, -0.5,
            0.5, -0.5,  0.5,
            0.5, -0.5,  0.5,
            -0.5, -0.5,  0.5,
            -0.5, -0.5, -0.5,

            -0.5,  0.5, -0.5,
            0.5,  0.5, -0.5,
            0.5,  0.5,  0.5,
            0.5,  0.5,  0.5,
            -0.5,  0.5,  0.5,
            -0.5,  0.5, -0.5
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
        # setup cube VAO
        self.cubeVAO = VertexArrayObject()
        self.cubeVBO = VertexBufferObject(self.cubeVertices)
        self.cubeVAO.setVertexBuffer(self.cubeVBO, 0, 0, 3 * sizeof(GLfloat))
        self.cubeVAO.setVertexAttribute(0, attribute_aPos)
        # setup screen VAO
        quad_aPos = VertexAttribute("aPos", 0, 2, GL_FLOAT, GL_FALSE, 0)
        quad_aTexCoord = VertexAttribute(
            "aTexCoords", 1, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(GLfloat))
        self.quadVAO = VertexArrayObject()
        self.quadVBO = VertexBufferObject(self.quadVertices)
        self.quadVAO.setVertexBuffer(self.quadVBO, 0, 0, 4 * sizeof(GLfloat))
        self.quadVAO.setVertexAttribute(0, quad_aPos)
        self.quadVAO.setVertexAttribute(0, quad_aTexCoord)

        # configure MSAA framebuffer
        self.framebuffer = Framebuffer()
        # create a multisampled color attachment texture
        self.textureColorBufferMultiSampled = Texture2DMultisample(
            4, GL_RGB32F, self.width, self.height)
        self.framebuffer.attachTexture2DMultisample(
            GL_COLOR_ATTACHMENT0, self.textureColorBufferMultiSampled, 0)
        # create a (also multisampled) renderbuffer object for depth and stencil attachments
        self.rbo = RenderbufferMultisample(
            4, GL_DEPTH24_STENCIL8, self.width, self.height)
        self.framebuffer.attachRenderbufferMultisample(
            GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, self.rbo)
        if self.framebuffer.isComplete() is not True:
            raise RuntimeError(
                'ERROR::FRAMEBUFFER:: Framebuffer is not complete!')
        # configure second post-processing framebuffer
        self.intermediateFBO = Framebuffer()
        self.screenTexture = Texture2D(1, GL_RGB16F, self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE)
        self.screenTexture.setFiltering(GL_LINEAR, GL_LINEAR)
        self.intermediateFBO.attachTexture2D(
            GL_COLOR_ATTACHMENT0, self.screenTexture, 0)
        if self.intermediateFBO.isComplete() is not True:
            raise RuntimeError(
                'ERROR::FRAMEBUFFER:: Intermediate framebuffer is not complete!')

        # shader configuration
        self.screenShader.use()
        self.screenShader.setUniform1i("screenTexture", 0)

    def cleanup(self) -> None:
        self.cubeVAO.delete()
        self.cubeVBO.delete()
        self.shader.delete()

    def render(self) -> None:
        super().render()
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 1. draw scene as normal in multisampled buffers
        self.framebuffer.bind()
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        # set transformation matrices
        self.shader.use()
        model = glm.mat4(1.0)
        view = self.camera.GetViewMatrix()
        projection = glm.perspective(
            glm.radians(self.camera.zoom), float(self.width/self.height), 0.1, 1000.0)
        self.shader.setUniformMatrix4fv("projection",projection)
        self.shader.setUniformMatrix4fv("view", view)
        self.shader.setUniformMatrix4fv("model", model)

        self.cubeVAO.bind()
        glDrawArrays(GL_TRIANGLES, 0, 36)

        # now blit multisampled buffer(s) to normal colorbuffer of intermediate FBO. Image is stored in screenTexture

        self.framebuffer.Blit(self.intermediateFBO, GL_COLOR_BUFFER_BIT, GL_NEAREST)

        # 3. now render quad with scene's visuals as its texture image
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glDisable(GL_DEPTH_TEST)

        # draw Screen quad
        self.screenShader.use()
        self.quadVAO.bind()
        self.screenTexture.bind(0)
        glDrawArrays(GL_TRIANGLES, 0, 6)    

if __name__ == "__main__":
    app = App()
    win = AntiAliaxingOffscreen(title="Hello, Offscreen!")
    app.run(win)