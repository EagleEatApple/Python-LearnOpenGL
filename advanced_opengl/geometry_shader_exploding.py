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
from learnopengl import Model


class GeometryShaderExploding(CameraWindow):


    def init(self) -> None:
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)

        # build and compile shaders
        # ------------------------------------
        self.shader = ProgramVGF("shaders/4/9.2.geometry_shader.vs",
                                "shaders/4/9.2.geometry_shader.gs",
                                "shaders/4/9.2.geometry_shader.fs")

        
        # load models
        # self.nanosuit = Model("objects/nanosuit/nanosuit.obj")
        self.nanosuit = Model("objects/backpack/backpack.obj")
        

    def cleanup(self) -> None:
        self.shader.delete()

    def render(self) -> None:
        super().render()
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # draw scene as normal
        projection = glm.perspective(
            glm.radians(45.0), float(self.width/self.height), 0.1, 100.0)
        model = glm.mat4(1.0)
        view = self.camera.GetViewMatrix()
        self.shader.use()
        self.shader.setUniformMatrix4fv("model", model)
        self.shader.setUniformMatrix4fv("view", view)
        self.shader.setUniformMatrix4fv("projection",projection)

        # add time component to geometry shader in the form of a uniform
        self.shader.setUniform1f("time", glfw.get_time())

        # draw model
        self.nanosuit.Draw(self.shader)
 
if __name__ == "__main__":
    app = App()
    win = GeometryShaderExploding(title="Hello, Geometry shader!")
    app.run(win)

