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


class Bloom(CameraWindow):


    def init(self) -> None:
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)

        # build and compile shaders
        # ------------------------------------
        self.shader = ProgramVF("shaders/5/7.bloom.vs",
                                "shaders/5/7.bloom.fs")
        self.shaderLight = ProgramVF("shaders/5/7.bloom.vs",
                                     "shaders/5/7.light_box.fs")
        self.shaderBlur = ProgramVF("shaders/5/7.blur.vs",
                                    "shaders/5/7.blur.fs")
        self.shaderBloomFinal = ProgramVF("shaders/5/7.bloom_final.vs",
                                          "shaders/5/7.bloom_final.fs")

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
        self.containerTexture = ImageTexture2D("textures/container2.png")
        self.containerTexture.setFiltering(GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR)
        self.containerTexture.setWrapMode(GL_REPEAT, GL_REPEAT)

        # configure floating point framebuffer
        self.hdrFBO = Framebuffer()
        # create 2 floating point color buffers (1 for normal rendering, other for brightness threshold values)
        self.colorBuffers : list[Texture2D] = []
        for i in range(2):
            tex = Texture2D(1, GL_RGBA16F, self.width, self.height, GL_RGBA, GL_FLOAT)
            tex.setFiltering(GL_LINEAR, GL_LINEAR)
            tex.setWrapMode(GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE)
            self.colorBuffers.append(tex)
            # attach texture to framebuffer
            self.hdrFBO.attachTexture2D(GL_COLOR_ATTACHMENT0 + i, self.colorBuffers[i], 0)

        #  create and attach depth buffer (renderbuffer)
        self.rboDepth = Renderbuffer(
            GL_DEPTH_COMPONENT16, self.width, self.height)
        self.hdrFBO.attachRenderbuffer(
            GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.rboDepth)
        # tell OpenGL which color attachments we'll use (of this framebuffer) for rendering
        attachments = [GL_COLOR_ATTACHMENT0, GL_COLOR_ATTACHMENT1]
        self.hdrFBO.setDrawBuffers(attachments)
        # glNamedFramebufferDrawBuffers(self.hdrFBO.fbo_id, 2, attachments)
        if self.hdrFBO.isComplete() is not True:
            raise RuntimeError('Framebuffer not complete!')
        
        # ping-pong-framebuffer for blurring
        self.pingpongFBO:list[Framebuffer] = []
        self.pingpongColorbuffers: list[Texture2D] = []
        for i in range(2):
            fbo = Framebuffer()
            tex = Texture2D(1, GL_RGBA16F, self.width, self.height, GL_RGBA, GL_FLOAT)
            tex.setFiltering(GL_LINEAR, GL_LINEAR)
            tex.setWrapMode(GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE)
            self.pingpongFBO.append(fbo)
            self.pingpongColorbuffers.append(tex)
            self.pingpongFBO[i].attachTexture2D(GL_COLOR_ATTACHMENT0, self.pingpongColorbuffers[i], 0)
            # also check if framebuffers are complete (no need for depth buffer)
            if self.pingpongFBO[i].isComplete() is not True:
                raise RuntimeError('Framebuffer not complete!')
        # lighting info
        # -------------
        # positions
        self.lightPositions = []
        self.lightPositions.append(glm.vec3( 0.0, 0.5,  1.5))
        self.lightPositions.append(glm.vec3(-4.0, 0.5, -3.0))
        self.lightPositions.append(glm.vec3( 3.0, 0.5,  1.0))
        self.lightPositions.append(glm.vec3(-.8,  2.4, -1.0))
        # colors
        self.lightColors = []
        self.lightColors.append(glm.vec3(5.0,   5.0,  5.0))
        self.lightColors.append(glm.vec3(10.0,  0.0,  0.0))
        self.lightColors.append(glm.vec3(0.0,   0.0,  15.0))
        self.lightColors.append(glm.vec3(0.0,   5.0,  0.0))

        # shader configuration
        # ---------------------
        self.shader.use()
        self.shader.setUniform1i("diffuseTexture", 0)
        self.shaderBlur.use()
        self.shaderBlur.setUniform1i("image", 0)
        self.shaderBloomFinal.use()
        self.shaderBloomFinal.setUniform1i("scene", 0)
        self.shaderBloomFinal.setUniform1i("bloomBlur", 1)

        self.bloom = True
        self.bloomKeyPressed = False
        self.exposure = 1.0
        self.camera.position = glm.vec3(0.0, 0.0, 5.0)

    def cleanup(self) -> None:

        self.woodTexture.delete()

    def render(self) -> None:
        super().render()
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 1. render scene into floating point framebuffer
        self.hdrFBO.bind()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        projection = glm.perspective(
            glm.radians(self.camera.zoom), float(self.width/self.height), 0.1, 100.0)
        view = self.camera.GetViewMatrix()
        self.shader.use()
        self.shader.setUniformMatrix4fv("view", view)
        self.shader.setUniformMatrix4fv("projection", projection)
        self.woodTexture.bind(0)
        # set lighting uniforms
        for i in range(len(self.lightPositions)):
            self.shader.setUniform3fv(
                "lights[" + str(i) + "].Position", self.lightPositions[i])
            self.shader.setUniform3fv(
                "lights[" + str(i) + "].Color", self.lightColors[i])
        self.shader.setUniform3fv("viewPos", self.camera.position)
        # create one large cube that acts as the floor
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(0.0, -1.0, 0.0))
        model = glm.scale(model, glm.vec3(12.5, 0.5, 12.5))
        self.shader.setUniformMatrix4fv("model", model)
        self.renderCube()

        # then create multiple cubes as the scenery
        self.containerTexture.bind(0)
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(0.0, 1.5, 0.0))
        model = glm.scale(model, glm.vec3(0.5))
        self.shader.setUniformMatrix4fv("model", model)
        self.renderCube()

        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(2.0, 0.0, 1.0))
        model = glm.scale(model, glm.vec3(0.5))
        self.shader.setUniformMatrix4fv("model",model)
        self.renderCube()

        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(-1.0, -1.0, 2.0))
        model = glm.rotate(model, glm.radians(60.0), glm.normalize(glm.vec3(1.0, 0.0, 1.0)))
        self.shader.setUniformMatrix4fv("model", model)
        self.renderCube()

        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(0.0, 2.7, 4.0))
        model = glm.rotate(model, glm.radians(23.0), glm.normalize(glm.vec3(1.0, 0.0, 1.0)))
        model = glm.scale(model, glm.vec3(1.25))
        self.shader.setUniformMatrix4fv("model", model)
        self.renderCube()

        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(-2.0, 1.0, -3.0))
        model = glm.rotate(model, glm.radians(124.0), glm.normalize(glm.vec3(1.0, 0.0, 1.0)))
        self.shader.setUniformMatrix4fv("model", model)
        self.renderCube()

        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(-3.0, 0.0, 0.0))
        model = glm.scale(model, glm.vec3(0.5))
        self.shader.setUniformMatrix4fv("model", model)
        self.renderCube()

        # finally show all the light sources as bright cubes
        self.shaderLight.use()
        self.shaderLight.setUniformMatrix4fv("view",view)
        self.shaderLight.setUniformMatrix4fv("projection", projection)

        for i in range(len(self.lightPositions)):
            model = glm.mat4(1.0)
            model = glm.translate(model, glm.vec3(self.lightPositions[i]))
            model = glm.scale(model, glm.vec3(0.25))
            self.shaderLight.setUniformMatrix4fv("model", model)
            self.shaderLight.setUniform3fv("lightColor", self.lightColors[i])
            self.renderCube()


        # 2. blur bright fragments with two-pass Gaussian Blur 
        # ----------------------------------------------------
        horizontal = True
        first_iteration = True
        amount = 10
        self.shaderBlur.use()
        for i in range(amount):
            self.pingpongFBO[int(horizontal)].bind()
            self.shaderBlur.setUniform1i("horizontal", horizontal)
            if first_iteration:
                self.colorBuffers[1].bind(0)
            else:
                self.pingpongColorbuffers[int(not horizontal)].bind(0)
            self.renderQuad()
            horizontal = not horizontal
            if first_iteration:
                first_iteration = False

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        # 3. now render floating point color buffer to 2D quad and tonemap HDR colors to default framebuffer's (clamped) color range
        # --------------------------------------------------------------------------------------------------------------------------
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.shaderBloomFinal.use()
        self.colorBuffers[0].bind(0)
        self.pingpongColorbuffers[int(not horizontal)].bind(1)
        self.shaderBloomFinal.setUniform1i("bloom", self.bloom)
        self.shaderBloomFinal.setUniform1f("exposure", self.exposure)
        self.renderQuad()
        print("bloom: " + ("on" if self.bloom else "off") + "| exposure: " + str(self.exposure))


    def renderCube(self) -> None:
        self.cubeVAO.bind()
        glDrawArrays(GL_TRIANGLES, 0, 36)

    def renderQuad(self) -> None:
        self.quadVAO.bind()
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    def key_input(self) -> None:
        if glfw.get_key(self.id, glfw.KEY_SPACE) == glfw.PRESS and not self.bloomKeyPressed:
            self.bloom = not self.bloom
            self.bloomKeyPressed = True
        if glfw.get_key(self.id, glfw.KEY_SPACE) == glfw.RELEASE:
            self.bloomKeyPressed = False

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
    win = Bloom(title="Hello, Bloom!")
    app.run(win)

