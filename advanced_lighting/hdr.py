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


class HDR(CameraWindow):


    def init(self) -> None:
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)

        # build and compile shaders
        # ------------------------------------
        self.shader = ProgramVF("shaders/5/6.lighting.vs",
                                "shaders/5/6.lighting.fs")
        

        self.hdrShader = ProgramVF("shaders/5/6.hdr.vs",
                                   "shaders/5/6.hdr.fs")
        
        # setup quad VAO
        self.quadVertices = np.array([
            # positions        # texture Coords
            -1.0,  1.0, 0.0, 0.0, 1.0,
            -1.0, -1.0, 0.0, 0.0, 0.0,
            1.0,  1.0, 0.0, 1.0, 1.0,
            1.0, -1.0, 0.0, 1.0, 0.0
        ], dtype=GLfloat)
        quad_aPos = VertexAttribute("aPos", 0, 3, GL_FLOAT, GL_FALSE, 0)
        quad_aTexCoord = VertexAttribute(
            "aTexCoords", 1, 2, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat))
        self.quadVAO = VertexArrayObject()
        self.quadVBO = VertexBufferObject(self.quadVertices)
        self.quadVAO.setVertexBuffer(self.quadVBO, 0, 0, 5 * sizeof(GLfloat))
        self.quadVAO.setVertexAttribute(0, quad_aPos)
        self.quadVAO.setVertexAttribute(0, quad_aTexCoord)

        # setup cube VAO
        self.cubeVertices = np.array([
            # back face
            -1.0, -1.0, -1.0,  0.0,  0.0, -1.0, 0.0, 0.0,  # bottom-left
            1.0,  1.0, -1.0,  0.0,  0.0, -1.0, 1.0, 1.0,  # top-right
            1.0, -1.0, -1.0,  0.0,  0.0, -1.0, 1.0, 0.0,  # bottom-right
            1.0,  1.0, -1.0,  0.0,  0.0, -1.0, 1.0, 1.0,  # top-right
            -1.0, -1.0, -1.0,  0.0,  0.0, -1.0, 0.0, 0.0,  # bottom-left
            -1.0,  1.0, -1.0,  0.0,  0.0, -1.0, 0.0, 1.0,  # top-left
            # front face
            -1.0, -1.0,  1.0,  0.0,  0.0,  1.0, 0.0, 0.0,  # bottom-left
            1.0, -1.0,  1.0,  0.0,  0.0,  1.0, 1.0, 0.0,  # bottom-right
            1.0,  1.0,  1.0,  0.0,  0.0,  1.0, 1.0, 1.0,  # top-right
            1.0,  1.0,  1.0,  0.0,  0.0,  1.0, 1.0, 1.0,  # top-right
            -1.0,  1.0,  1.0,  0.0,  0.0,  1.0, 0.0, 1.0,  # top-left
            -1.0, -1.0,  1.0,  0.0,  0.0,  1.0, 0.0, 0.0,  # bottom-left
            # left face
            -1.0,  1.0,  1.0, -1.0,  0.0,  0.0, 1.0, 0.0,  # top-right
            -1.0,  1.0, -1.0, -1.0,  0.0,  0.0, 1.0, 1.0,  # top-left
            -1.0, -1.0, -1.0, -1.0,  0.0,  0.0, 0.0, 1.0,  # bottom-left
            -1.0, -1.0, -1.0, -1.0,  0.0,  0.0, 0.0, 1.0,  # bottom-left
            -1.0, -1.0,  1.0, -1.0,  0.0,  0.0, 0.0, 0.0,  # bottom-right
            -1.0,  1.0,  1.0, -1.0,  0.0,  0.0, 1.0, 0.0,  # top-right
            # right face
            1.0,  1.0,  1.0,  1.0,  0.0,  0.0, 1.0, 0.0,  # top-left
            1.0, -1.0, -1.0,  1.0,  0.0,  0.0, 0.0, 1.0,  # bottom-right
            1.0,  1.0, -1.0,  1.0,  0.0,  0.0, 1.0, 1.0,  # top-right
            1.0, -1.0, -1.0,  1.0,  0.0,  0.0, 0.0, 1.0,  # bottom-right
            1.0,  1.0,  1.0,  1.0,  0.0,  0.0, 1.0, 0.0,  # top-left
            1.0, -1.0,  1.0,  1.0,  0.0,  0.0, 0.0, 0.0,  # bottom-left
            # bottom face
            -1.0, -1.0, -1.0,  0.0, -1.0,  0.0, 0.0, 1.0,  # top-right
            1.0, -1.0, -1.0,  0.0, -1.0,  0.0, 1.0, 1.0,  # top-left
            1.0, -1.0,  1.0,  0.0, -1.0,  0.0, 1.0, 0.0,  # bottom-left
            1.0, -1.0,  1.0,  0.0, -1.0,  0.0, 1.0, 0.0,  # bottom-left
            -1.0, -1.0,  1.0,  0.0, -1.0,  0.0, 0.0, 0.0,  # bottom-right
            -1.0, -1.0, -1.0,  0.0, -1.0,  0.0, 0.0, 1.0,  # top-right
            # top face
            -1.0,  1.0, -1.0,  0.0,  1.0,  0.0, 0.0, 1.0,  # top-left
            1.0,  1.0, 1.0,  0.0,  1.0,  0.0, 1.0, 0.0,  # bottom-right
            1.0,  1.0, -1.0,  0.0,  1.0,  0.0, 1.0, 1.0,  # top-right
            1.0,  1.0,  1.0,  0.0,  1.0,  0.0, 1.0, 0.0,  # bottom-right
            -1.0,  1.0, -1.0,  0.0,  1.0,  0.0, 0.0, 1.0,  # top-left
            -1.0,  1.0,  1.0,  0.0,  1.0,  0.0, 0.0, 0.0  # bottom-left
        ], dtype=GLfloat)
        self.cubeVAO = VertexArrayObject()
        self.VBO = VertexBufferObject(self.cubeVertices)
        cube_aPos = VertexAttribute("aPos", 0, 3, GL_FLOAT, GL_FALSE, 0)
        cube_aNormal = VertexAttribute(
            "aNormal", 1, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat))
        cube_aTexCoords = VertexAttribute(
            "aTexCoords", 2, 2, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat))
        self.cubeVAO.setVertexBuffer(self.VBO, 0, 0, 8 * sizeof(GLfloat))
        self.cubeVAO.setVertexAttribute(0, cube_aPos)
        self.cubeVAO.setVertexAttribute(0, cube_aNormal)
        self.cubeVAO.setVertexAttribute(0, cube_aTexCoords)

        # load textures
        self.woodTexture = ImageTexture2D("textures/wood.png")
        self.woodTexture.setFiltering(GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR)
        self.woodTexture.setWrapMode(GL_REPEAT, GL_REPEAT)

        # configure floating point framebuffer
        self.hdrFBO = Framebuffer()
        # create floating point color buffer
        self.colorBuffer = Texture2D(
            1, GL_RGBA16F, self.width, self.height, GL_RGBA, GL_FLOAT)
        self.colorBuffer.setFiltering(GL_LINEAR, GL_LINEAR)

        #  create depth buffer (renderbuffer)
        self.rboDepth = Renderbuffer(
            GL_DEPTH_COMPONENT16, self.width, self.height)
        # attach buffers
        self.hdrFBO.attachTexture2D(GL_COLOR_ATTACHMENT0, self.colorBuffer, 0)
        self.hdrFBO.attachRenderbuffer(
            GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.rboDepth)
        if self.hdrFBO.isComplete() is not True:
            raise RuntimeError('Framebuffer not complete!')

        # lighting info
        # -------------
        # positions
        self.lightPositions = []
        self.lightPositions.append(glm.vec3(0.0,  0.0, 49.5))  # back light
        self.lightPositions.append(glm.vec3(-1.4, -1.9, 9.0))
        self.lightPositions.append(glm.vec3(0.0, -1.8, 4.0))
        self.lightPositions.append(glm.vec3(0.8, -1.7, 6.0))
        # colors
        self.lightColors = []
        self.lightColors.append(glm.vec3(200.0, 200.0, 200.0))
        self.lightColors.append(glm.vec3(0.1, 0.0, 0.0))
        self.lightColors.append(glm.vec3(0.0, 0.0, 0.2))
        self.lightColors.append(glm.vec3(0.0, 0.1, 0.0))

        # shader configuration
        # ---------------------
        self.shader.use()
        self.shader.setUniform1i("diffuseTexture", 0)
        self.hdrShader.use()
        self.hdrShader.setUniform1i("hdrBuffer", 0)

        self.hdr = True
        self.hdrKeyPressed = False
        self.exposure = 1.0
        self.camera.position = glm.vec3(0.0, 0.0, 5.0)

    def cleanup(self) -> None:

        self.woodTexture.delete()
        self.hdrShader.delete()

    def render(self) -> None:
        super().render()
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 1. render scene into floating point framebuffer
        self.hdrFBO.bind()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        projection = glm.perspective(
            glm.radians(self.camera.zoom), float(self.width/self.height), 0.1, 100.0)
        view = self.camera.GetViewMatrix()
        self.shader.use()
        self.shader.setUniformMatrix4fv("view", view)
        self.shader.setUniformMatrix4fv("projection",projection)
        self.woodTexture.bind(0)
        # set lighting uniforms
        for i in range(len(self.lightPositions)):
            self.shader.setUniform3fv("lights[" + str(i) + "].Position", self.lightPositions[i])
            self.shader.setUniform3fv("lights[" + str(i) + "].Color", self.lightColors[i])

        self.shader.setUniform3fv("viewPos", self.camera.position)
        # render tunnel
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(0.0, 0.0, 25.0))
        model = glm.scale(model, glm.vec3(2.5, 2.5, 27.5))
        self.shader.setUniformMatrix4fv("model", model)
        self.shader.setUniform1i("inverse_normals", True)
        self.renderCube()
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # 2. now render floating point color buffer to 2D quad and tonemap HDR colors to default framebuffer's (clamped) color range
        # --------------------------------------------------------------------------------------------------------------------------
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.hdrShader.use()
        self.colorBuffer.bind(0)
        self.hdrShader.setUniform1i("hdr", self.hdr)
        self.hdrShader.setUniform1f("exposure", self.exposure)
        self.renderQuad()
        print("hdr: " + ("on" if self.hdr else "off") + "| exposure: " + str(self.exposure))



    
    def renderCube(self) -> None:
        self.cubeVAO.bind()
        glDrawArrays(GL_TRIANGLES, 0, 36)

    def renderQuad(self) -> None:
        self.quadVAO.bind()
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

 
    def key_input(self) -> None:
        if glfw.get_key(self.id, glfw.KEY_SPACE) == glfw.PRESS and not self.hdrKeyPressed:
            self.hdr = not self.hdr
            self.hdrKeyPressed = True
        if glfw.get_key(self.id, glfw.KEY_SPACE) == glfw.RELEASE:
            self.hdrKeyPressed = False

        if glfw.get_key(self.id, glfw.KEY_Q) == glfw.PRESS:
            if self.exposure > 0.0:
                self.exposure -= 0.001
            else:
                self.exposure = 0.0
        if glfw.get_key(self.id, glfw.KEY_E) == glfw.PRESS:
            self.exposure += 0.001

        super().key_input()


if __name__ == "__main__":
    app = App()
    win = HDR(title="Hello, HDR!")
    app.run(win)
