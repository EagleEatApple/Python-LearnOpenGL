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
from learnopengl import Model


class ModelLoading(CameraWindow):


    def init(self) -> None:

        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)

        # build and compile our shader program
        # ------------------------------------
        self.ourShader = ProgramVF("shaders/3/1.model_loading.vs", "shaders/3/1.model_loading.fs")

        self.ourModel = Model("objects/backpack/backpack.obj")

    def cleanup(self) -> None:
        self.ourShader.delete()

    def render(self) -> None:
        super().render()
        glClearColor(0.05, 0.05, 0.05, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #  don't forget to enable shader before setting uniforms
        self.ourShader.use()

        # view/projection transformations
        projection = glm.perspective(
            glm.radians(self.camera.zoom), float(self.width) / self.height, 0.1, 100.0)
        view = self.camera.GetViewMatrix()
        self.ourShader.setUniformMatrix4fv("projection",projection)
        self.ourShader.setUniformMatrix4fv("view", view)

        # render the loaded model
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(0.0, 0.0, 0.0))
        model = glm.scale(model, glm.vec3(1.0, 1.0, 1.0))
        self.ourShader.setUniformMatrix4fv("model", model)
        self.ourModel.Draw(self.ourShader)

if __name__ == "__main__":
    app = App()
    win = ModelLoading(title="Hello, Model!")
    app.run(win)