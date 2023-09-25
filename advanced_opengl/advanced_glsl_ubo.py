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


class AdvancedGLSLUBO(CameraWindow):


    def init(self) -> None:
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)

        # build and compile shaders
        # ------------------------------------
        self.shaderRed = ProgramVF("shaders/4/8.advanced_glsl.vs",
                                "shaders/4/8.red.fs")

        self.shaderGreen = ProgramVF("shaders/4/8.advanced_glsl.vs",
                                "shaders/4/8.green.fs")

        self.shaderBlue = ProgramVF("shaders/4/8.advanced_glsl.vs",
                                "shaders/4/8.blue.fs")

        self.shaderYellow = ProgramVF("shaders/4/8.advanced_glsl.vs",
                                "shaders/4/8.yellow.fs")


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


        # vertex attributes
        attribute_aPos = VertexAttribute("aPos", 0, 3, GL_FLOAT, GL_FALSE, 0)
        # cube VAO
        self.cubeVAO = VertexArrayObject()
        self.cubeVBO = VertexBufferObject(self.cubeVertices)
        self.cubeVAO.setVertexBuffer(self.cubeVBO, 0, 0, 3 * sizeof(GLfloat))
        self.cubeVAO.setVertexAttribute(0, attribute_aPos)

        # configure a uniform buffer object and define the range of the buffer that links to a uniform binding point
        self.uboMatrices = UniformBufferObject(0, 2 * glm.sizeof(glm.mat4))
        # then we link each shader's uniform block to this uniform binding point
        self.shaderRed.setUBOBinding("Matrices", 0)
        self.shaderGreen.setUBOBinding("Matrices", 0)
        self.shaderBlue.setUBOBinding("Matrices", 0)
        self.shaderYellow.setUBOBinding("Matrices", 0)


        # store the projection matrix (we only do this once now) (note: we're not using zoom anymore by changing the FoV)
        projection = glm.perspective(45.0, float(self.width) / self.height, 0.1, 100.0)
        self.uboMatrices.update(0, glm.sizeof(glm.mat4), glm.value_ptr(projection))

    def cleanup(self) -> None:
        self.cubeVAO.delete()
        self.cubeVBO.delete()
        self.shaderRed.delete()

    def render(self) -> None:
        super().render()
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # set the view and projection matrix in the uniform block - we only have to do this once per loop iteration.
        view = self.camera.GetViewMatrix()
        self.uboMatrices.update(glm.sizeof(glm.mat4), glm.sizeof(glm.mat4), glm.value_ptr(view))

        # draw 4 cubes 
        # RED
        glBindVertexArray(self.cubeVAO.vao_id)
        self.shaderRed.use()
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(-0.75, 0.75, 0.0)) # move top-left
        self.shaderRed.setUniformMatrix4fv("model", model)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        # GREEN
        self.shaderGreen.use()
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(0.75, 0.75, 0.0)) # move top-right
        self.shaderGreen.setUniformMatrix4fv("model", model)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        # YELLOW
        self.shaderYellow.use()
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(-0.75, -0.75, 0.0)) # move bottom-left
        self.shaderYellow.setUniformMatrix4fv("model", model)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        # BLUE
        self.shaderBlue.use()
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(0.75, -0.75, 0.0)) # move bottom-right
        self.shaderBlue.setUniformMatrix4fv("model", model)
        glDrawArrays(GL_TRIANGLES, 0, 36)
 
if __name__ == "__main__":
    app = App()
    win = AdvancedGLSLUBO(title="Hello, UBO!")
    app.run(win)

