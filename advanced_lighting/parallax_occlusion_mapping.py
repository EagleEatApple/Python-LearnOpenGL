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


class ParallaxOcclusionMapping(CameraWindow):


    def init(self) -> None:
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)

        # build and compile shaders
        # ------------------------------------
        self.shader = ProgramVF("shaders/5/5.3.parallax_mapping.vs",
                                "shaders/5/5.3.parallax_mapping.fs")

        # load textures
        self.diffuseMap = ImageTexture2D("textures/bricks2.jpg")
        self.diffuseMap.setFiltering(GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR)
        self.diffuseMap.setWrapMode(GL_REPEAT, GL_REPEAT)
        self.normalMap = ImageTexture2D("textures/bricks2_normal.jpg")
        self.normalMap.setFiltering(GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR)
        self.normalMap.setWrapMode(GL_REPEAT, GL_REPEAT)
        self.heightMap = ImageTexture2D("textures/bricks2_disp.jpg")
        self.heightMap.setFiltering(GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR)
        self.heightMap.setWrapMode(GL_REPEAT, GL_REPEAT)

        # shader configuration
        # ---------------------
        self.shader.use()
        self.shader.setUniform1i("diffuseMap", 0)
        self.shader.setUniform1i("normalMap", 1)
        self.shader.setUniform1i("depthMap", 2)

        # lighting info
        self.lightPos = glm.vec3(0.5, 1.0, 0.3)
        self.heightScale = 0.1

        # quad data
        # positions
        pos1 = glm.vec3(-1.0,  1.0, 0.0)
        pos2 = glm.vec3(-1.0, -1.0, 0.0)
        pos3 = glm.vec3( 1.0, -1.0, 0.0)
        pos4 = glm.vec3( 1.0,  1.0, 0.0)
        # texture coordinates
        uv1 = glm.vec2(0.0, 1.0)
        uv2 = glm.vec2(0.0, 0.0)
        uv3 = glm.vec2(1.0, 0.0)
        uv4 = glm.vec2(1.0, 1.0)
        # normal vector
        nm = glm.vec3(0.0, 0.0, 1.0)

        # calculate tangent/bitangent vectors of both triangles
        tangent1 = glm.vec3()
        tangent2 = glm.vec3()
        bitangent1 = glm.vec3()
        bitangent2 = glm.vec3()
        # triangle 1
        # ----------
        edge1 = pos2 - pos1
        edge2 = pos3 - pos1
        deltaUV1 = uv2 - uv1
        deltaUV2 = uv3 - uv1

        f = 1.0 / (deltaUV1.x * deltaUV2.y - deltaUV2.x * deltaUV1.y)

        tangent1.x = f * (deltaUV2.y * edge1.x - deltaUV1.y * edge2.x)
        tangent1.y = f * (deltaUV2.y * edge1.y - deltaUV1.y * edge2.y)
        tangent1.z = f * (deltaUV2.y * edge1.z - deltaUV1.y * edge2.z)
        tangent1 = glm.normalize(tangent1)

        bitangent1.x = f * (-deltaUV2.x * edge1.x + deltaUV1.x * edge2.x)
        bitangent1.y = f * (-deltaUV2.x * edge1.y + deltaUV1.x * edge2.y)
        bitangent1.z = f * (-deltaUV2.x * edge1.z + deltaUV1.x * edge2.z)
        bitangent1 = glm.normalize(bitangent1)

        # triangle 2
        # ----------
        edge1 = pos3 - pos1
        edge2 = pos4 - pos1
        deltaUV1 = uv3 - uv1
        deltaUV2 = uv4 - uv1

        f = 1.0 / (deltaUV1.x * deltaUV2.y - deltaUV2.x * deltaUV1.y)

        tangent2.x = f * (deltaUV2.y * edge1.x - deltaUV1.y * edge2.x)
        tangent2.y = f * (deltaUV2.y * edge1.y - deltaUV1.y * edge2.y)
        tangent2.z = f * (deltaUV2.y * edge1.z - deltaUV1.y * edge2.z)
        tangent2 = glm.normalize(tangent2)

        bitangent2.x = f * (-deltaUV2.x * edge1.x + deltaUV1.x * edge2.x)
        bitangent2.y = f * (-deltaUV2.x * edge1.y + deltaUV1.x * edge2.y)
        bitangent2.z = f * (-deltaUV2.x * edge1.z + deltaUV1.x * edge2.z)
        bitangent2 = glm.normalize(bitangent2)

        self.quadVertices = np.array([
            # positions            # normal         # texcoords  # tangent                          # bitangent
            pos1.x, pos1.y, pos1.z, nm.x, nm.y, nm.z, uv1.x, uv1.y, tangent1.x, tangent1.y, tangent1.z, bitangent1.x, bitangent1.y, bitangent1.z,
            pos2.x, pos2.y, pos2.z, nm.x, nm.y, nm.z, uv2.x, uv2.y, tangent1.x, tangent1.y, tangent1.z, bitangent1.x, bitangent1.y, bitangent1.z,
            pos3.x, pos3.y, pos3.z, nm.x, nm.y, nm.z, uv3.x, uv3.y, tangent1.x, tangent1.y, tangent1.z, bitangent1.x, bitangent1.y, bitangent1.z,

            pos1.x, pos1.y, pos1.z, nm.x, nm.y, nm.z, uv1.x, uv1.y, tangent2.x, tangent2.y, tangent2.z, bitangent2.x, bitangent2.y, bitangent2.z,
            pos3.x, pos3.y, pos3.z, nm.x, nm.y, nm.z, uv3.x, uv3.y, tangent2.x, tangent2.y, tangent2.z, bitangent2.x, bitangent2.y, bitangent2.z,
            pos4.x, pos4.y, pos4.z, nm.x, nm.y, nm.z, uv4.x, uv4.y, tangent2.x, tangent2.y, tangent2.z, bitangent2.x, bitangent2.y, bitangent2.z
        ], dtype=GLfloat)
        # configure plane VAO
        quad_aPos = VertexAttribute("aPos", 0, 3, GL_FLOAT, GL_FALSE, 0)
        quad_aNormal = VertexAttribute("aNormal", 1, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat))
        quad_aTexCoords = VertexAttribute(
            "aTexCoords", 2, 2, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat))
        quad_aTangent = VertexAttribute(
            "aTangent", 3, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat))
        quad_aBitangent = VertexAttribute(
            "aBitangent", 4, 3, GL_FLOAT, GL_FALSE, 11 * sizeof(GLfloat))
        self.quadVAO = VertexArrayObject()
        self.quadVBO = VertexBufferObject(self.quadVertices)
        self.quadVAO.setVertexBuffer(self.quadVBO, 0, 0, 14 * sizeof(GLfloat))
        self.quadVAO.setVertexAttribute(0, quad_aPos)
        self.quadVAO.setVertexAttribute(0, quad_aNormal)
        self.quadVAO.setVertexAttribute(0, quad_aTexCoords)
        self.quadVAO.setVertexAttribute(0, quad_aTangent)
        self.quadVAO.setVertexAttribute(0, quad_aBitangent)

    def cleanup(self) -> None:
        self.diffuseMap.delete()
        self.shader.delete()

    def render(self) -> None:
        super().render()
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # configure view/projection matrices
        self.shader.use()
        view = self.camera.GetViewMatrix()
        projection = glm.perspective(
            glm.radians(self.camera.zoom), float(self.width/self.height), 0.1, 100.0)
        self.shader.setUniformMatrix4fv("view", view)
        self.shader.setUniformMatrix4fv("projection",projection)

        # render parallax-mapped quad
        model = glm.mat4(1.0)
        model = glm.rotate(model, glm.radians(glfw.get_time() * -10.0), glm.normalize(glm.vec3(1.0, 0.0, 1.0))) # rotate the quad to show normal mapping from multiple directions
        self.shader.setUniformMatrix4fv("model", model)
        self.shader.setUniform3fv("viewPos", self.camera.position)
        self.shader.setUniform3fv("lightPos", self.lightPos)
        self.shader.setUniform1f("heightScale", self.heightScale)
        print(self.heightScale)
        self.diffuseMap.bind(0)
        self.normalMap.bind(1)
        self.heightMap.bind(2)
        self.renderQuad()

        # render light source (simply re-renders a smaller plane at the light's position for debugging/visualization)
        model = glm.mat4(1.0)
        model = glm.translate(model, self.lightPos)
        model = glm.scale(model, glm.vec3(0.1))
        self.shader.setUniformMatrix4fv("model", model)
        self.renderQuad()


    def renderQuad(self) -> None:
        self.quadVAO.bind()
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 6)

    def key_input(self) -> None:
        if glfw.get_key(self.id, glfw.KEY_Q) == glfw.PRESS:
            if self.heightScale > 0.0:
                self.heightScale -= 0.0005
            else:
                self.heightScale = 0.0
        if glfw.get_key(self.id, glfw.KEY_E) == glfw.PRESS:
            if self.heightScale < 1.0:
                self.heightScale += 0.0005
            else:
                self.heightScale = 1.0
        super().key_input()


if __name__ == "__main__":
    app = App()
    win = ParallaxOcclusionMapping(title="Hello, Parallax mapping!")
    app.run(win)