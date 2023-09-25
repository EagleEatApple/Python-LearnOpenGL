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


class StencilTesting(CameraWindow):


    def init(self) -> None:
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glEnable(GL_STENCIL_TEST)
        glStencilFunc(GL_NOTEQUAL, 1, 0xFF)
        glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)

        # build and compile shaders
        # ------------------------------------
        self.shader = ProgramVF("shaders/4/2.stencil_testing.vs",
                                "shaders/4/2.stencil_testing.fs")

        self.shaderSingleColor = ProgramVF("shaders/4/2.stencil_testing.vs",
                                "shaders/4/2.stencil_single_color.fs")

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
        # don't forget to clear the stencil buffer!
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)

        # set uniforms
        self.shaderSingleColor.use()
        model = glm.mat4(1.0)
        view = self.camera.GetViewMatrix()
        projection = glm.perspective(
            glm.radians(self.camera.zoom), float(self.width/self.height), 0.1, 100.0)
        self.shaderSingleColor.setUniformMatrix4fv("view", view)
        self.shaderSingleColor.setUniformMatrix4fv("projection",projection)

        self.shader.use()
        self.shader.setUniformMatrix4fv("view", view)
        self.shader.setUniformMatrix4fv("projection",projection)

        # draw floor as normal, but don't write the floor to the stencil buffer
        # we only care about the containers. We set its mask to 0x00 to not 
        # write to the stencil buffer.
        glStencilMask(0x00)
        # floor
        self.planeVAO.bind()
        self.floorTexture.bind(0)
        model = glm.mat4(1.0)
        self.shader.setUniformMatrix4fv("model", model)
        glDrawArrays(GL_TRIANGLES, 0, 6)


        # 1st. render pass, draw objects as normal, writing to the stencil buffer
        # --------------------------------------------------------------------
        glStencilFunc(GL_ALWAYS, 1, 0xFF)
        glStencilMask(0xFF)
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


        # 2nd. render pass: now draw slightly scaled versions of the objects, this time disabling stencil writing.
        # Because the stencil buffer is now filled with several 1s. The parts of the buffer that are 1 are not drawn, thus only drawing 
        # the objects' size differences, making it look like borders.
        # -----------------------------------------------------------------------------------------------------------------------------
        glStencilFunc(GL_NOTEQUAL, 1, 0xFF)
        glStencilMask(0x00)
        glDisable(GL_DEPTH_TEST)
        self.shaderSingleColor.use()
        scale = 1.1
        # cubes
        self.cubeVAO.bind()
        self.cubeTexture.bind(0)
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(-1.0, 0.0, -1.0))
        model = glm.scale(model, glm.vec3(scale, scale, scale))
        self.shaderSingleColor.setUniformMatrix4fv("model", model)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(2.0, 0.0, 0.0))
        model = glm.scale(model, glm.vec3(scale, scale, scale))
        self.shaderSingleColor.setUniformMatrix4fv("model", model)
        glDrawArrays(GL_TRIANGLES, 0, 36)

        glStencilMask(0xFF)
        glStencilFunc(GL_ALWAYS, 0, 0xFF)
        glEnable(GL_DEPTH_TEST)
 
if __name__ == "__main__":
    app = App()
    win = StencilTesting(title="Hello, Stencil testing!")
    app.run(win)

