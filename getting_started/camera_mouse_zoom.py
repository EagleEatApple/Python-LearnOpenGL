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

class CameraMouseZooom(GLWindow):
    def init(self) -> None:
        self.cameraPos = glm.vec3(0, 0, 3.0)
        self.cameraFront = glm.vec3(0, 0, -1)
        self.cameraUp = glm.vec3(0, 1.0, 0)
        self.firstMouse = True
        self.width, self.height = glfw.get_window_size(self.id)
        self.lastX = float(self.width)/2
        self.lastY = float(self.height)/2
        self.yaw = -90.0
        self.pitch = 0.0
        self.fov = 45.0
        self.deltaTime = 0.0
        self.lastFrame = 0.0
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)
        
        # build and compile our shader program
        # ------------------------------------
        self.ourShader = ProgramVF("shaders/1/7.3.camera.vs", 
                                   "shaders/1/7.3.camera.fs")

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

    def cleanup(self) -> None:
        self.VAO.delete()
        self.VBO.delete()
        self.texture1.delete()
        self.texture2.delete()
        self.ourShader.delete()

    def render(self) -> None:
        currentFrame = glfw.get_time()
        self.deltaTime = currentFrame - self.lastFrame
        self.lastFrame = currentFrame
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # also clear the depth buffer now!

        # bind textures on corresponding texture units
        
        self.texture1.bind(0)
        
        self.texture2.bind(1)

        # activate shader
        self.ourShader.use()

        # pass projection matrix to shader (note that in this case it could change every frame)
        projection = glm.perspective(
            glm.radians(self.fov), float(self.width)/self.height, 0.1, 100.0)
        self.ourShader.setUniformMatrix4fv("projection",projection)

        # camera/view transformation
        view = glm.lookAt(self.cameraPos, self.cameraPos + self.cameraFront, self.cameraUp)
        self.ourShader.setUniformMatrix4fv("view", view)

        # render boxes
        self.VAO.bind()
        for i in range(0,10):
            # calculate the model matrix for each object and pass it to shader before drawing
            model = glm.mat4(1.0) # make sure to initialize matrix to identity matrix first
            model = glm.translate(model, self.cubePositions[i])
            angle = 20.0 * i
            model = glm.rotate(model, glm.radians(angle), glm.vec3(1.0, 0.3, 0.5))
            self.ourShader.setUniformMatrix4fv("model", model)
            glDrawArrays(GL_TRIANGLES, 0, 36)

    def key_input(self)-> None:
        if glfw.get_key(self.id, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(self.id, True)
        cameraSpeed = 25.0 * self.deltaTime
        if glfw.get_key(self.id, glfw.KEY_W) == glfw.PRESS:
            self.cameraPos += cameraSpeed * self.cameraFront
        if glfw.get_key(self.id, glfw.KEY_S) == glfw.PRESS:
            self.cameraPos -= cameraSpeed * self.cameraFront
        if glfw.get_key(self.id, glfw.KEY_A) == glfw.PRESS:
            self.cameraPos -= glm.normalize(glm.cross(self.cameraFront, self.cameraUp)) * cameraSpeed
        if glfw.get_key(self.id, glfw.KEY_D) == glfw.PRESS:
            self.cameraPos += glm.normalize(glm.cross(self.cameraFront, self.cameraUp)) * cameraSpeed

    def mouse_move(self, window, xpos, ypos)->None:
        if self.firstMouse:
            self.lastX = xpos
            self.lastY = ypos
            self.firstMouse = False

        xoffset = xpos - self.lastX
        yoffset = self.lastY - ypos

        self.lastX = xpos
        self.lastY = ypos
        sensitivity = 0.1
        xoffset *= sensitivity
        yoffset *= sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89.0:
            self.pitch = -89.0

        front = glm.vec3()
        front.x = cos(glm.radians(self.yaw)) * cos(glm.radians(self.pitch))
        front.y = sin(glm.radians(self.pitch))
        front.z = sin(glm.radians(self.yaw)) * cos(glm.radians(self.pitch))
        self.cameraFront = glm.normalize(front)


    def mouse_wheel(self, window, xoffset, yoffset)-> None:
        self.fov -= yoffset
        if self.fov < 1.0:
            self.fov = 1.0
        if self.fov > 45.0:
            self.fov = 45.0

if __name__ == "__main__":
    app = App()
    win = CameraMouseZooom(title="Hello, Camera!")
    app.run(win)