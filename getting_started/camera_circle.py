import sys
parent_dir = "../Python-LearnOpenGL"
sys.path.append(parent_dir)

from math import sin, cos

from OpenGL.GL import *
import numpy as np
import glm
import glfw

from app import *
from py3gl4 import *


class CameraCircle(GLWindow):
    def init(self) -> None:
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)
        
        # build and compile our shader program
        # ------------------------------------
        self.ourShader = ProgramVF("shaders/1/7.1.camera.vs", 
                                   "shaders/1/7.1.camera.fs")

        # set up vertex data (and buffer(s)) and configure vertex attributes
        # ------------------------------------------------------------------
        self.vertices = np.array([
        -0.5, -0.5, -0.5, 0.0, 0.0,
        0.5, -0.5, -0.5, 1.0, 0.0,
        0.5, 0.5, -0.5, 1.0, 1.0,
        0.5, 0.5, -0.5, 1.0, 1.0,
        -0.5, 0.5, -0.5, 0.0, 1.0,
        -0.5, -0.5, -0.5, 0.0, 0.0,

        -0.5, -0.5, 0.5, 0.0, 0.0,
        0.5, -0.5, 0.5, 1.0, 0.0,
        0.5, 0.5, 0.5, 1.0, 1.0,
        0.5, 0.5, 0.5, 1.0, 1.0,
        -0.5, 0.5, 0.5, 0.0, 1.0,
        -0.5, -0.5, 0.5, 0.0, 0.0,

        -0.5, 0.5, 0.5, 1.0, 0.0,
        -0.5, 0.5, -0.5, 1.0, 1.0,
        -0.5, -0.5, -0.5, 0.0, 1.0,
        -0.5, -0.5, -0.5, 0.0, 1.0,
        -0.5, -0.5, 0.5, 0.0, 0.0,
        -0.5, 0.5, 0.5, 1.0, 0.0,

        0.5, 0.5, 0.5, 1.0, 0.0,
        0.5, 0.5, -0.5, 1.0, 1.0,
        0.5, -0.5, -0.5, 0.0, 1.0,
        0.5, -0.5, -0.5, 0.0, 1.0,
        0.5, -0.5, 0.5, 0.0, 0.0,
        0.5, 0.5, 0.5, 1.0, 0.0,

        -0.5, -0.5, -0.5, 0.0, 1.0,
        0.5, -0.5, -0.5, 1.0, 1.0,
        0.5, -0.5, 0.5, 1.0, 0.0,
        0.5, -0.5, 0.5, 1.0, 0.0,
        -0.5, -0.5, 0.5, 0.0, 0.0,
        -0.5, -0.5, -0.5, 0.0, 1.0,

        -0.5, 0.5, -0.5, 0.0, 1.0,
        0.5, 0.5, -0.5, 1.0, 1.0,
        0.5, 0.5, 0.5, 1.0, 0.0,
        0.5, 0.5, 0.5, 1.0, 0.0,
        -0.5, 0.5, 0.5, 0.0, 0.0,
        -0.5, 0.5, -0.5, 0.0, 1.0
        ], dtype=GLfloat)
        # world space positions of our cubes
        self.cubePositions = [
            glm.vec3( 0.0,  0.0,  0.0),
            glm.vec3( 2.0,  5.0, -15.0),
            glm.vec3(-1.5, -2.2, -2.5),
            glm.vec3(-3.8, -2.0, -12.3),
            glm.vec3( 2.4, -0.4, -3.5),
            glm.vec3(-1.7,  3.0, -7.5),
            glm.vec3( 1.3, -2.0, -2.5),
            glm.vec3( 1.5,  2.0, -2.5),
            glm.vec3( 1.5,  0.2, -1.5),
            glm.vec3(-1.3,  1.0, -1.5)
        ]

        self.VAO = VertexArrayObject()
        self.VBO = VertexBufferObject(self.vertices)

        attribute_aPos = VertexAttribute("aPos", 0, 3, GL_FLOAT, GL_FALSE, 0)
        attribute_aTexCoord = VertexAttribute("aTexCoord", 1, 2, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat))
        self.VAO.setVertexBuffer(self.VBO, 0, 0, 5 * sizeof(GLfloat))
        self.VAO.setVertexAttribute(0, attribute_aPos)
        self.VAO.setVertexAttribute(0, attribute_aTexCoord)

        # load and create a texture
        self.texture1 = ImageTexture2D("textures/container.jpg")
        self.texture2 = ImageTexture2D("textures/awesomeface.png",True)

        # tell opengl for each sampler to which texture unit it belongs to (only has to be done once)
        # -------------------------------------------------------------------------------------------
        self.ourShader.use()
        self.ourShader.setUniform1i("texture1", 0)
        self.ourShader.setUniform1i("texture2", 1)

        # pass projection matrix to shader (as projection matrix rarely changes there's no need to do this per frame)
        # -----------------------------------------------------------------------------------------------------------
        width, height = glfw.get_window_size(self.id)
        projection = glm.perspective(
            glm.radians(45.0), float(width/height), 0.1, 100.0)
        self.ourShader.setUniformMatrix4fv("projection",projection)
        
    def cleanup(self) -> None:
        self.VAO.delete()
        self.VBO.delete()
        self.texture1.delete()
        self.texture2.delete()
        self.ourShader.delete()

    def render(self) -> None:
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # also clear the depth buffer now!

        # bind textures on corresponding texture units
        self.texture1.bind(0)
        self.texture2.bind(1)

        # activate shader
        self.ourShader.use()

        # camera/view transformation
        view = glm.mat4(1.0) # make sure to initialize matrix to identity matrix first
        radius = 10.0
        camX = sin(glfw.get_time()) * radius
        camZ = cos(glfw.get_time()) * radius
        view = glm.lookAt(glm.vec3(camX, 0.0, camZ), glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0))
        self.ourShader.setUniformMatrix4fv("view", view)

        # render boxes
        self.VAO.bind()
        for i in range(0,10):
            model = glm.mat4(1.0)
            model = glm.translate(model, self.cubePositions[i])
            angle = 20.0 * i
            model = glm.rotate(model, glm.radians(angle), glm.vec3(1.0, 0.3, 0.5))
            self.ourShader.setUniformMatrix4fv("model", model)
            glDrawArrays(GL_TRIANGLES, 0, 36)

if __name__ == "__main__":
    app = App()
    win = CameraCircle(title="Hello, Camera!")
    app.run(win)