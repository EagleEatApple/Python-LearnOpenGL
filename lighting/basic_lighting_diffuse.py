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


class BasicLightingDiffuse(CameraWindow):


    def init(self) -> None:

        # lighting
        self.lightPos = glm.vec3(1.2, 1.0, 2.0)

        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)
        
        # build and compile our shader program
        # ------------------------------------

        self.lightingShader = ProgramVF("shaders/2/2.1.basic_lighting.vs", 
                                   "shaders/2/2.1.basic_lighting.fs")

        self.lightCubeShader = ProgramVF("shaders/2/2.1.light_cube.vs", 
                                   "shaders/2/2.1.light_cube.fs")

        # set up vertex data (and buffer(s)) and configure vertex attributes
        # ------------------------------------------------------------------
        self.vertices = np.array([
        -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,
         0.5, -0.5, -0.5,  0.0,  0.0, -1.0,
         0.5,  0.5, -0.5,  0.0,  0.0, -1.0,
         0.5,  0.5, -0.5,  0.0,  0.0, -1.0,
        -0.5,  0.5, -0.5,  0.0,  0.0, -1.0,
        -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,

        -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,
         0.5, -0.5,  0.5,  0.0,  0.0,  1.0,
         0.5,  0.5,  0.5,  0.0,  0.0,  1.0,
         0.5,  0.5,  0.5,  0.0,  0.0,  1.0,
        -0.5,  0.5,  0.5,  0.0,  0.0,  1.0,
        -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,

        -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,
        -0.5,  0.5, -0.5, -1.0,  0.0,  0.0,
        -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,
        -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,
        -0.5, -0.5,  0.5, -1.0,  0.0,  0.0,
        -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,

         0.5,  0.5,  0.5,  1.0,  0.0,  0.0,
         0.5,  0.5, -0.5,  1.0,  0.0,  0.0,
         0.5, -0.5, -0.5,  1.0,  0.0,  0.0,
         0.5, -0.5, -0.5,  1.0,  0.0,  0.0,
         0.5, -0.5,  0.5,  1.0,  0.0,  0.0,
         0.5,  0.5,  0.5,  1.0,  0.0,  0.0,

        -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,
         0.5, -0.5, -0.5,  0.0, -1.0,  0.0,
         0.5, -0.5,  0.5,  0.0, -1.0,  0.0,
         0.5, -0.5,  0.5,  0.0, -1.0,  0.0,
        -0.5, -0.5,  0.5,  0.0, -1.0,  0.0,
        -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,

        -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,
         0.5,  0.5, -0.5,  0.0,  1.0,  0.0,
         0.5,  0.5,  0.5,  0.0,  1.0,  0.0,
         0.5,  0.5,  0.5,  0.0,  1.0,  0.0,
        -0.5,  0.5,  0.5,  0.0,  1.0,  0.0,
        -0.5,  0.5, -0.5,  0.0,  1.0,  0.0
        ], dtype=GLfloat)

        # first, configure the cube's VAO (and VBO)
        self.cubeVAO = VertexArrayObject()
        self.VBO = VertexBufferObject(self.vertices)
        # position attribute
        attribute_aPos = VertexAttribute("aPos", 0, 3, GL_FLOAT, GL_FALSE, 0)
        # normal attribute
        attribute_aNormal = VertexAttribute("aNormal", 1, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat))
        self.cubeVAO.setVertexBuffer(self.VBO, 0, 0, 6 * sizeof(GLfloat))
        self.cubeVAO.setVertexAttribute(0, attribute_aPos)
        self.cubeVAO.setVertexAttribute(0, attribute_aNormal)

        # second, configure the light's VAO (VBO stays the same; the vertices are the same for the light object which is also a 3D cube)
        self.lightCubeVAO = VertexArrayObject()
        self.lightCubeVAO.setVertexBuffer(self.VBO, 0, 0, 6 * sizeof(GLfloat))
        self.lightCubeVAO.setVertexAttribute(0, attribute_aPos)

    def cleanup(self) -> None:
        self.cubeVAO.delete()
        self.lightCubeVAO.delete()
        self.VBO.delete()
        self.lightCubeShader.delete()
        self.lightingShader.delete()


    def render(self) -> None:
        super().render()
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # be sure to activate shader when setting uniforms/drawing objects
        self.lightingShader.use()
        self.lightingShader.setUniform3f("objectColor", 1.0, 0.5, 0.31)
        self.lightingShader.setUniform3f("lightColor", 1.0, 1.0, 1.0)
        self.lightingShader.setUniform3fv("lightPos", self.lightPos)

        # view/projection transformations
        projection = glm.perspective(
            glm.radians(self.camera.zoom), float(self.width/self.height), 0.1, 100.0)
        view = self.camera.GetViewMatrix()
        self.lightingShader.setUniformMatrix4fv("projection",projection)
        self.lightingShader.setUniformMatrix4fv("view", view)

        # world transformation
        model = glm.mat4(1.0)
        self.lightingShader.setUniformMatrix4fv("model", model)

        # render the cube
        self.cubeVAO.bind()
        glDrawArrays(GL_TRIANGLES, 0, 36)

        # also draw the lamp object
        self.lightCubeShader.use()
        self.lightCubeShader.setUniformMatrix4fv("projection",projection)
        self.lightCubeShader.setUniformMatrix4fv("view", view)
        model = glm.mat4(1.0)
        model = glm.translate(model, self.lightPos)
        model = glm.scale(model, glm.vec3(0.2))
        self.lightCubeShader.setUniformMatrix4fv("model", model)
        self.lightCubeVAO.bind()
        glDrawArrays(GL_TRIANGLES, 0, 36)

    
 
if __name__ == "__main__":
    app = App()
    win = BasicLightingDiffuse(title="Hello, Light!")
    app.run(win)