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


class PointShadows(CameraWindow):


    def init(self) -> None:
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        # build and compile shaders
        # ------------------------------------
        self.shader = ProgramVF("shaders/5/3.2.1.point_shadows.vs",
                                "shaders/5/3.2.1.point_shadows.fs")
        
        self.simpleDepthShader = ProgramVGF("shaders/5/3.2.1.point_shadows_depth.vs", 
        "shaders/5/3.2.1.point_shadows_depth.gs",
        "shaders/5/3.2.1.point_shadows_depth.fs" )
        

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

        # configure depth map FBO
        self.SHADOW_WIDTH = 1024
        self.SHADOW_HEIGHT = 1024
        self.depthMapFBO = Framebuffer()
        self.depthCubemap = TextureCubemap(GL_DEPTH_COMPONENT24, self.SHADOW_WIDTH, self.SHADOW_HEIGHT)
        self.depthCubemap.setFiltering(GL_NEAREST, GL_NEAREST)
        self.depthCubemap.setWrapMode(GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE)
        # attach depth texture as FBO's depth buffer
        self.depthMapFBO.attachTextureCubemap(GL_DEPTH_ATTACHMENT, self.depthCubemap, 0)
        self.depthMapFBO.setDrawBuffer(GL_NONE)
        self.depthMapFBO.setReadBuffer(GL_NONE)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # shader configuration
        # ---------------------
        self.shader.use()
        self.shader.setUniform1i("diffuseTexture", 0)
        self.shader.setUniform1i("depthMap", 1)

        # lighting info
        self.lightPos = glm.vec3(0.0, 0.0, 0.0)
        self.shadows = True
        self.shadowsKeyPressed = False

    def cleanup(self) -> None:

        self.woodTexture.delete()
        self.simpleDepthShader.delete()

    def render(self) -> None:
        super().render()
        # move light position over time
        self.lightPos.z = sin(glfw.get_time() * 0.5) * 3.0
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        near_plane = 1.0
        far_plane  = 25.0
        shadowProj = glm.perspective(glm.radians(90.0), float(self.SHADOW_WIDTH / self.SHADOW_HEIGHT), near_plane, far_plane)
        shadowTransforms = []
        shadowTransforms.append(shadowProj * glm.lookAt(self.lightPos, self.lightPos + glm.vec3( 1.0,  0.0,  0.0), glm.vec3(0.0, -1.0,  0.0)))
        shadowTransforms.append(shadowProj * glm.lookAt(self.lightPos, self.lightPos + glm.vec3(-1.0,  0.0,  0.0), glm.vec3(0.0, -1.0,  0.0)))
        shadowTransforms.append(shadowProj * glm.lookAt(self.lightPos, self.lightPos + glm.vec3( 0.0,  1.0,  0.0), glm.vec3(0.0,  0.0,  1.0)))
        shadowTransforms.append(shadowProj * glm.lookAt(self.lightPos, self.lightPos + glm.vec3( 0.0, -1.0,  0.0), glm.vec3(0.0,  0.0, -1.0)))
        shadowTransforms.append(shadowProj * glm.lookAt(self.lightPos, self.lightPos + glm.vec3( 0.0,  0.0,  1.0), glm.vec3(0.0, -1.0,  0.0)))
        shadowTransforms.append(shadowProj * glm.lookAt(self.lightPos, self.lightPos + glm.vec3( 0.0,  0.0, -1.0), glm.vec3(0.0, -1.0,  0.0)))


        # 1. render scene to depth cubemap
        glViewport(0, 0, self.SHADOW_WIDTH, self.SHADOW_HEIGHT)
        self.depthMapFBO.bind()
        glClear(GL_DEPTH_BUFFER_BIT)
        self.simpleDepthShader.use()
        for i in range(6):
            matrix = "".join(["shadowMatrices[", str(i), "]"])
            self.simpleDepthShader.setUniformMatrix4fv(matrix, shadowTransforms[i])
        self.simpleDepthShader.setUniform1f("far_plane", far_plane)
        self.simpleDepthShader.setUniform3fv("lightPos", self.lightPos)
        self.renderScene(self.simpleDepthShader)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # 2. render scene as normal
        glViewport(0, 0, self.width, self.height)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.shader.use()
        view = self.camera.GetViewMatrix()
        projection = glm.perspective(
            glm.radians(self.camera.zoom), float(self.width/self.height), 0.1, 100.0)
        self.shader.setUniformMatrix4fv("view", view)
        self.shader.setUniformMatrix4fv("projection",projection)  
        # set light uniforms
        self.shader.setUniform3fv("viewPos", self.camera.position)
        self.shader.setUniform3fv("lightPos", self.lightPos) 
        self.shader.setUniform1i("shadows", self.shadows)
        self.shader.setUniform1f("far_plane", far_plane)
        self.woodTexture.bind(0)
        self.depthCubemap.bind(1)
        self.renderScene(self.shader)

    def renderScene(self, shader:Program) -> None:
        # room cube
        model = glm.mat4(1.0)
        model = glm.scale(model, glm.vec3(5.0))
        shader.setUniformMatrix4fv("model", model)
        glDisable(GL_CULL_FACE)
        shader.setUniform1i("reverse_normals", 1)
        self.renderCube()
        shader.setUniform1i("reverse_normals", 0)
        glEnable(GL_CULL_FACE)       
        # cubes
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(4.0, -3.5, 0.0))
        model = glm.scale(model, glm.vec3(0.5))
        shader.setUniformMatrix4fv("model", model)
        self.renderCube()
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(2.0, 3.0, 1.0))
        model = glm.scale(model, glm.vec3(0.75))
        shader.setUniformMatrix4fv("model", model)
        self.renderCube()
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(-3.0, -1.0, 0.0))
        model = glm.scale(model, glm.vec3(0.5))
        shader.setUniformMatrix4fv("model", model)
        self.renderCube()
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(-1.5, 1.0, 1.5))
        model = glm.scale(model, glm.vec3(0.5))
        shader.setUniformMatrix4fv("model", model)
        self.renderCube()

        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(-1.5, 2.0, -3.0))
        model = glm.rotate(model, glm.radians(
            60.0), glm.normalize(glm.vec3(1.0, 0.0, 1.0)))
        model = glm.scale(model, glm.vec3(0.75))
        shader.setUniformMatrix4fv("model", model)
        self.renderCube()

    def renderCube(self) -> None:
        self.cubeVAO.bind()
        glDrawArrays(GL_TRIANGLES, 0, 36)

    def key_input(self) -> None:
        if glfw.get_key(self.id, glfw.KEY_SPACE) == glfw.PRESS and not self.shadowsKeyPressed:
            self.shadows = not self.shadows
            self.shadowsKeyPressed = True
        if glfw.get_key(self.id, glfw.KEY_SPACE) == glfw.RELEASE:
            self.shadowsKeyPressed = False
        super().key_input()
 
if __name__ == "__main__":
    app = App()
    win = PointShadows(title="Hello, Point shadows!")
    app.run(win)
