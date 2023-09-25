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


class NormalVisualization(CameraWindow):


    def init(self) -> None:
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)

        # build and compile shaders
        # ------------------------------------
        self.shader = ProgramVF("shaders/4/9.3.default.vs",
                                "shaders/4/9.3.default.fs")

        self.normalShader = ProgramVGF("shaders/4/9.3.normal_visualization.vs",    
                                "shaders/4/9.3.normal_visualization.gs",
                                "shaders/4/9.3.normal_visualization.fs")

        # load models
        # self.nanosuit = Model("objects/nanosuit/nanosuit.obj")
        self.nanosuit = Model("objects/backpack/backpack.obj")
        

    def cleanup(self) -> None:
        self.shader.delete()

    def render(self) -> None:
        super().render()
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # configure transformation matrices
        projection = glm.perspective(
            glm.radians(45.0), float(self.width/self.height), 0.1, 100.0)
        model = glm.mat4(1.0)
        view = self.camera.GetViewMatrix()
        self.shader.use()
        self.shader.setUniformMatrix4fv("model", model)
        self.shader.setUniformMatrix4fv("view", view)
        self.shader.setUniformMatrix4fv("projection",projection)

        # draw model as usual
        self.nanosuit.Draw(self.shader)

        # then draw model with normal visualizing geometry shader
        self.normalShader.use()
        self.normalShader.setUniformMatrix4fv("model", model)
        self.normalShader.setUniformMatrix4fv("view", view)
        self.normalShader.setUniformMatrix4fv("projection",projection)
        
        self.nanosuit.Draw(self.normalShader)
 
if __name__ == "__main__":
    app = App()
    win = NormalVisualization(title="Hello, Normal!")
    app.run(win)
