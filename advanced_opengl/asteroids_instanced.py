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


class AsteroidsInstanced(CameraWindow):


    def init(self) -> None:
        self.camera.position = glm.vec3(0.0, 20.0, 155.0)
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)

        # build and compile shaders
        # ------------------------------------
        self.asteroidShader = ProgramVF("shaders/4/10.3.asteroids.vs",
                                "shaders/4/10.3.asteroids.fs")

        self.planetShader = ProgramVF("shaders/4/10.3.planet.vs",
                                        "shaders/4/10.3.planet.fs")

        
        # load models
        self.rock = Model("objects/rock/rock.obj")  
        self.planet = Model("objects/planet/planet.obj")

        # generate a large list of semi-random model transformation matrices
        self.amount = 100000
        modelMatrices = []
        random.seed()
        radius = 150.0
        offset = 25.0
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
            model = glm.transpose(model)  # apply for numpy

            # 4. now add to list of matrices
            # self.modelMatrices[i] = model 
            modelMatrices.append(model)       

        # configure instanced array
        instanced_buffer = np.array(modelMatrices)
        buffer = VertexBufferObject(instanced_buffer)

        # set transformation matrices as an instance vertex attribute (with divisor 1)
        # note: we're cheating a little by taking the, now publicly declared, VAO of the model's mesh(es) and adding new vertexAttribPointers
        # normally you'd want to do this in a more organized fashion, but for learning purposes this will do.
        # -----------------------------------------------------------------------------------------------------------------------------------
        for i in range(len(self.rock.meshes)):
            VAO = self.rock.meshes[i].VAO
            VAO.bind()
            # set attribute pointers for matrix (4 times vec4)
            attribute_aInstanceMatrix1 = VertexAttribute("aInstanceMatrix", 3, 4, GL_FLOAT, GL_FALSE, 0)
            attribute_aInstanceMatrix2 = VertexAttribute("aInstanceMatrix", 4, 4, GL_FLOAT, GL_FALSE, glm.sizeof(glm.vec4))
            attribute_aInstanceMatrix3 = VertexAttribute("aInstanceMatrix", 5, 4, GL_FLOAT, GL_FALSE, 2 * glm.sizeof(glm.vec4))
            attribute_aInstanceMatrix4 = VertexAttribute("aInstanceMatrix", 6, 4, GL_FLOAT, GL_FALSE, 3 * glm.sizeof(glm.vec4))
            VAO.setVertexBuffer(buffer, 5, 0, glm.sizeof(glm.mat4))
            VAO.setVertexAttribute(5, attribute_aInstanceMatrix1)
            VAO.setVertexAttribute(5, attribute_aInstanceMatrix2)
            VAO.setVertexAttribute(5, attribute_aInstanceMatrix3)
            VAO.setVertexAttribute(5, attribute_aInstanceMatrix4)
            VAO.setBindingDivisor(5,1)


    def cleanup(self) -> None:
        pass

    def render(self) -> None:
        super().render()
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # configure transformation matrices
        projection = glm.perspective(
            glm.radians(45.0), float(self.width/self.height), 0.1, 1000.0)
        view = self.camera.GetViewMatrix()
        self.asteroidShader.use()
        self.asteroidShader.setUniformMatrix4fv("view", view)
        self.asteroidShader.setUniformMatrix4fv("projection",projection)
        self.planetShader.use()
        self.planetShader.setUniformMatrix4fv("view", view)
        self.planetShader.setUniformMatrix4fv("projection",projection)
        
        # draw planet
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(0.0, -3.0, 0.0))
        model = glm.scale(model, glm.vec3(4.0, 4.0, 4.0))
        self.planetShader.setUniformMatrix4fv("model", model)
        self.planet.Draw(self.planetShader)

        # draw meteorites
        self.asteroidShader.use()
        self.asteroidShader.setUniform1i("texture_diffuse1", 0)
        self.rock.textures_loaded[0].tex.bind(0)
        for i in range(len(self.rock.meshes)):
            self.rock.meshes[i].VAO.bind()
            glDrawElementsInstanced(GL_TRIANGLES, len(self.rock.meshes[i].indices), GL_UNSIGNED_INT, None, self.amount)
 
if __name__ == "__main__":
    app = App()
    win = AsteroidsInstanced(title="Hello, Asteroids!")
    app.run(win)


