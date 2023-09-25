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


class ShadowMapping(CameraWindow):


    def init(self) -> None:
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)

        # build and compile shaders
        # ------------------------------------
        self.shader = ProgramVF("shaders/5/3.1.3.shadow_mapping.vs",
                                "shaders/5/3.1.3.shadow_mapping.fs")

        self.simpleDepthShader = ProgramVF("shaders/5/3.1.3.shadow_mapping_depth.vs",
                                           "shaders/5/3.1.3.shadow_mapping_depth.fs")

        self.debugDepthQuad = ProgramVF("shaders/5/3.1.3.debug_quad.vs",
                                        "shaders/5/3.1.3.debug_quad_depth.fs")

        # set up vertex data (and buffer(s)) and configure vertex attributes
        # ------------------------------------------------------------------

        self.planeVertices = np.array([
            # positions         # normals    # texcoords
            25.0, -0.5,  25.0,  0.0, 1.0, 0.0,  25.0,  0.0,
            -25.0, -0.5,  25.0,  0.0, 1.0, 0.0,   0.0,  0.0,
            -25.0, -0.5, -25.0,  0.0, 1.0, 0.0,   0.0, 25.0,

            25.0, -0.5,  25.0,  0.0, 1.0, 0.0,  25.0,  0.0,
            -25.0, -0.5, -25.0,  0.0, 1.0, 0.0,   0.0, 25.0,
            25.0, -0.5, -25.0,  0.0, 1.0, 0.0,  25.0, 25.0
        ], dtype=GLfloat)

        # vertex attributes
        attribute_aPos = VertexAttribute("aPos", 0, 3, GL_FLOAT, GL_FALSE, 0)
        attribute_aNormal = VertexAttribute(
            "aNormal", 1, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat))
        attribute_aTexCoords = VertexAttribute(
            "aTexCoords", 2, 2, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat))

        # plane VAO
        self.planeVAO = VertexArrayObject()
        self.planeVBO = VertexBufferObject(self.planeVertices)
        self.planeVAO.setVertexBuffer(self.planeVBO, 0, 0, 8 * sizeof(GLfloat))
        self.planeVAO.setVertexAttribute(0, attribute_aPos)
        self.planeVAO.setVertexAttribute(0, attribute_aNormal)
        self.planeVAO.setVertexAttribute(0, attribute_aTexCoords)

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

        # configure depth map FBO
        self.SHADOW_WIDTH = 1024
        self.SHADOW_HEIGHT = 1024
        self.depthMapFBO = Framebuffer()
        self.depthMap = Texture2D(
            1, GL_DEPTH_COMPONENT32F, self.SHADOW_WIDTH, self.SHADOW_HEIGHT, GL_DEPTH_COMPONENT, GL_FLOAT)
        self.depthMap.setFiltering(GL_NEAREST, GL_NEAREST)
        self.depthMap.setWrapMode(GL_CLAMP_TO_BORDER, GL_CLAMP_TO_BORDER)
        boarderColor = glm.vec4(1.0, 1.0, 1.0, 1.0)
        self.depthMap.setBorderColor(boarderColor)
        # attach depth texture as FBO's depth buffer
        self.depthMapFBO.attachTexture2D(GL_DEPTH_ATTACHMENT, self.depthMap, 0)
        self.depthMapFBO.setDrawBuffer(GL_NONE)
        self.depthMapFBO.setReadBuffer(GL_NONE)


        # shader configuration
        # ---------------------
        self.shader.use()
        self.shader.setUniform1i("diffuseTexture", 0)
        self.shader.setUniform1i("shadowMap", 1)
        self.debugDepthQuad.use()
        self.debugDepthQuad.setUniform1i("depthMap", 0)

        # lighting info
        self.lightPos = glm.vec3(-2.0, 4.0, -1.0)

    def cleanup(self) -> None:

        self.planeVAO.delete()
        self.planeVBO.delete()

        self.woodTexture.delete()
        self.simpleDepthShader.delete()

    def render(self) -> None:
        super().render()
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 1. render depth of scene to texture (from light's perspective)
        near_plane = 1.0
        far_plane = 7.5
        lightProjection = glm.ortho(-10.0, 10.0, -
                                    10.0, 10.0, near_plane, far_plane)
        lightView = glm.lookAt(self.lightPos, glm.vec3(
            0.0), glm.vec3(0.0, 1.0, 0.0))
        lightSpaceMatrix = lightProjection * lightView
        # render scene from light's point of view
        self.simpleDepthShader.use()
        self.simpleDepthShader.setUniformMatrix4fv("lightSpaceMatrix", lightSpaceMatrix)

        glViewport(0, 0, self.SHADOW_WIDTH, self.SHADOW_HEIGHT)
        self.depthMapFBO.bind()
        glClear(GL_DEPTH_BUFFER_BIT)
        self.woodTexture.bind(0)
        self.renderScene(self.simpleDepthShader)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # reset viewport
        glViewport(0, 0, self.width, self.height)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 2. render scene as normal using the generated depth/shadow map  
        # --------------------------------------------------------------
        self.shader.use()
        view = self.camera.GetViewMatrix()
        projection = glm.perspective(
            glm.radians(self.camera.zoom), float(self.width/self.height), 0.1, 100.0)
        self.shader.setUniformMatrix4fv("view", view)
        self.shader.setUniformMatrix4fv("projection",projection)  
        # set light uniforms
        self.shader.setUniform3fv("viewPos", self.camera.position)
        self.shader.setUniform3fv("lightPos", self.lightPos) 
        self.shader.setUniformMatrix4fv("lightSpaceMatrix", lightSpaceMatrix)
        self.woodTexture.bind(0)
        self.depthMap.bind(1)
        self.renderScene(self.shader)

        # render Depth map to quad for visual debugging
        # ---------------------------------------------
        self.debugDepthQuad.use()

        self.debugDepthQuad.setUniform1f("near_plane", near_plane)
        self.debugDepthQuad.setUniform1f("far_plane", far_plane)
        self.depthMap.bind(0)
        # self.renderQuad()

    def renderScene(self, shader: ProgramVF) -> None:
        # floor
        model = glm.mat4(1.0)
        shader.setUniformMatrix4fv("model", model)
        self.planeVAO.bind()
        glDrawArrays(GL_TRIANGLES, 0, 6)
        # cubes
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(0.0, 1.5, 0.0))
        model = glm.scale(model, glm.vec3(0.5))
        shader.setUniformMatrix4fv("model", model)
        self.renderCube()
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(2.0, 0.0, 1.0))
        model = glm.scale(model, glm.vec3(0.5))
        shader.setUniformMatrix4fv("model", model)
        self.renderCube()
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(-1.0, 0.0, 2.0))
        model = glm.rotate(model, glm.radians(
            60.0), glm.normalize(glm.vec3(1.0, 0.0, 1.0)))
        model = glm.scale(model, glm.vec3(0.25))
        shader.setUniformMatrix4fv("model", model)
        self.renderCube()

    def renderCube(self) -> None:
        self.cubeVAO.bind()
        glDrawArrays(GL_TRIANGLES, 0, 36)


    def renderQuad(self) -> None:
        self.quadVAO.bind()
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

 
if __name__ == "__main__":
    app = App()
    win = ShadowMapping(title="Hello, Shadow mapping!")
    app.run(win)
