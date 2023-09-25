import sys
parent_dir = "../Python-LearnOpenGL"
sys.path.append(parent_dir)

from OpenGL.GL import *
import numpy as np
import glm
import glfw

from py3gl4 import *
from app import *

class CoordinateSystems(GLWindow):
    def init(self) -> None:
        # build and compile our shader program
        # ------------------------------------
        self.ourShader = ProgramVF("shaders/1/6.1.coordinate_systems.vs", 
                                   "shaders/1/6.1.coordinate_systems.fs")
        # set up vertex data (and buffer(s)) and configure vertex attributes
        # ------------------------------------------------------------------
        self.vertices = np.array([
            # positions      texture coords
            0.5,  0.5, 0.0,  1.0, 1.0, # top right
            0.5, -0.5, 0.0,  1.0, 0.0,    # bottom right
            -0.5, -0.5, 0.0,  0.0, 0.0,  # bottom left
            -0.5,  0.5, 0.0,  0.0, 1.0   # top
        ], dtype=GLFLOAT)
        self.indices = np.array([
            0, 1, 3,  # first Triangle
            1, 2, 3  # second Triangle
        ], dtype=GLUINT)

        self.VAO = VertexArrayObject()
        self.VBO = VertexBufferObject(self.vertices)
        self.EBO = ElementBufferObject(self.indices)
        attribute_aPos = VertexAttribute("aPos", 0, 3, GL_FLOAT, GL_FALSE, 0)
        attribute_aTexCoord = VertexAttribute("aTexCoord", 1, 2, GL_FLOAT, GL_FALSE, 3 * sizeof(GLFLOAT))
        self.VAO.setVertexBuffer(self.VBO, 0, 0, 5 * sizeof(GLFLOAT))
        self.VAO.setVertexAttribute(0, attribute_aPos)
        self.VAO.setVertexAttribute(0, attribute_aTexCoord)
        self.VAO.setElementBuffer(self.EBO)

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
        self.EBO.delete()
        self.texture1.delete()
        self.texture2.delete()
        self.ourShader.delete()

    def render(self) -> None:
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # bind textures on corresponding texture units
        self.texture1.bind(0)
        self.texture2.bind(1)

        # activate shader
        self.ourShader.use()

        # create transformations
        model = glm.mat4(1.0) # make sure to initialize matrix to identity matrix first
        view = glm.mat4(1.0)
        projection = glm.mat4(1.0)
        model = glm.rotate(model, glm.radians(-55.0), glm.vec3(1.0, 0.0, 0.0))
        view = glm.translate(view, glm.vec3(0.0, 0.0, -3.0))
        width, height = glfw.get_window_size(self.id)
        projection = glm.perspective(
            glm.radians(45.0), float(width/height), 0.1, 100.0)

        self.ourShader.setUniformMatrix4fv("model", model)
        self.ourShader.setUniformMatrix4fv("view", view)
        # note: currently we set the projection matrix each frame, but since the projection matrix rarely changes it's often best practice to set it outside the main loop only once.
        self.ourShader.setUniformMatrix4fv("projection",projection)


        # render container
        self.VAO.bind()
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, ctypes.c_void_p(0))

if __name__ == "__main__":
    app = App()
    win = CoordinateSystems(title="Hello, Coordinate Systems!")
    app.run(win)