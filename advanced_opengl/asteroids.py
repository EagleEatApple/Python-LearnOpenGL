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


class Asteroids(CameraWindow):


    def init(self) -> None:
        self.camera.position = glm.vec3(0.0, 20.0, 55.0)
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)

        # build and compile shaders
        # ------------------------------------
        self.shader = ProgramVF("shaders/4/10.2.instancing.vs",
                                "shaders/4/10.2.instancing.fs")

        # load models
        self.rock = Model("objects/rock/rock.obj")
        self.planet = Model("objects/planet/planet.obj")

        # generate a large list of semi-random model transformation matrices
        self.amount = 1000
        self.modelMatrices = []
        random.seed()
        radius = 50.0
        offset = 2.5
        for i in range(self.amount):
            model = glm.mat4(1.0)
            # 1. translation: displace along circle with 'radius' in range [-offset, offset]
            angle = float(i) / self.amount * 360.0
            displacement = random.uniform(-offset, offset)
            x = sin(angle) * radius + displacement
            displacement = random.uniform(-offset, offset)
            y = displacement * 0.4 # keep height of asteroid field smaller compared to width of x and z
            displacement = random.uniform(-offset, offset)
            z = cos(angle) * radius + displacement
            model = glm.translate(model, glm.vec3(x, y, z))

            # 2. scale: Scale between 0.05 and 0.25
            scale = random.uniform(0.05, 0.25)
            model = glm.scale(model, glm.vec3(scale))

            # 3. rotation: add random rotation around a (semi)randomly picked rotation axis vector
            rotAngle = random.uniform(0, 360)
            model = glm.rotate(model, rotAngle, glm.vec3(0.4, 0.6, 0.8))

            # 4. now add to list of matrices
            self.modelMatrices.append(model)

    def cleanup(self) -> None:
        self.shader.delete()

    def render(self) -> None:
        super().render()
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # configure transformation matrices
        projection = glm.perspective(
            glm.radians(45.0), float(self.width/self.height), 0.1, 1000.0)
        view = self.camera.GetViewMatrix()
        self.shader.use()
        self.shader.setUniformMatrix4fv("view", view)
        self.shader.setUniformMatrix4fv("projection",projection)

        
        # draw planet
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(0.0, -3.0, 0.0))
        model = glm.scale(model, glm.vec3(4.0, 4.0, 4.0))
        self.shader.setUniformMatrix4fv("model", model)
        self.planet.Draw(self.shader)

        # draw meteorites
        for modelMatrix in self.modelMatrices:
            self.shader.setUniformMatrix4fv("model", modelMatrix)
            self.rock.Draw(self.shader)
 
if __name__ == "__main__":
    app = App()
    win = Asteroids(title="Hello, Asteroids!")
    app.run(win)

