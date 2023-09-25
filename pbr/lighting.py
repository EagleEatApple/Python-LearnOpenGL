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

class Lighting(CameraWindow):


    def init(self) -> None:
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)

        # build and compile shaders
        # ------------------------------------
        self.shader = ProgramVF("shaders/6/1.1.pbr.vs",
                                "shaders/6/1.1.pbr.fs")

        # set up vertex data (and buffer(s)) and configure vertex attributes
        # ------------------------------------------------------------------
        positions = []
        uv = []
        normals = []
        indices = []
        X_SEGMENTS = 64
        Y_SEGMENTS = 64
        PI = 3.14159265359
        for x in range(X_SEGMENTS + 1):
            for y in range(Y_SEGMENTS + 1):
                xSegment = x / X_SEGMENTS
                ySegment = y / Y_SEGMENTS
                xPos = cos(xSegment * 2.0 * PI) * sin(ySegment * PI)
                yPos = cos(ySegment * PI)
                zPos = sin(xSegment * 2.0 * PI) * sin(ySegment * PI)
                positions.append(glm.vec3(xPos, yPos, zPos))
                uv.append(glm.vec2(xSegment, ySegment))
                normals.append(glm.vec3(xPos, yPos, zPos))

        oddRow = False
        for y in range(Y_SEGMENTS):
            if (not oddRow): # even rows: y == 0, y == 2 and so on
                for x in range(X_SEGMENTS + 1):
                    indices.append(y       * (X_SEGMENTS + 1) + x)
                    indices.append((y + 1) * (X_SEGMENTS + 1) + x)
            else:
                for x in range(X_SEGMENTS, -1, -1):
                    indices.append((y + 1) * (X_SEGMENTS + 1) + x)
                    indices.append(y       * (X_SEGMENTS + 1) + x)

            oddRow = not oddRow
        self.indexCount = len(indices)
        number_vertex = len(positions)
        dataArray = np.empty((number_vertex, 8), dtype=GLfloat)
        indicesArray = np.array(indices)
        for i in range(number_vertex):
            dataArray[i, 0] = positions[i].x
            dataArray[i, 1] = positions[i].y
            dataArray[i, 2] = positions[i].z
            dataArray[i, 3] = normals[i].x
            dataArray[i, 4] = normals[i].y
            dataArray[i, 5] = normals[i].z
            dataArray[i, 6] = uv[i].x
            dataArray[i, 7] = uv[i].y

        self.sphereVAO = VertexArrayObject()
        vbo = VertexBufferObject(dataArray)
        ebo = ElementBufferObject(indicesArray)
        attribute_aPos = VertexAttribute("aPos", 0, 3, GL_FLOAT, GL_FALSE, 0)
        attribute_aNormal = VertexAttribute("aNormal", 1, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat))
        attribute_aTexCoords = VertexAttribute(
            "aTexCoords", 2, 2, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat))
        self.sphereVAO.setVertexBuffer(vbo, 0, 0, 8 * sizeof(GLfloat))
        self.sphereVAO.setVertexAttribute(0, attribute_aPos)
        self.sphereVAO.setVertexAttribute(0, attribute_aNormal)
        self.sphereVAO.setVertexAttribute(0, attribute_aTexCoords)
        self.sphereVAO.setElementBuffer(ebo)


        # shader configuration
        # ---------------------
        self.shader.use()
        self.shader.setUniform3f("albedo", 0.5, 0.0, 0.0)
        self.shader.setUniform1f("ao", 1.0)

        # lights
        # ------
        self.lightPositions = [
            glm.vec3(-10.0,  10.0, 10.0),
            glm.vec3( 10.0,  10.0, 10.0),
            glm.vec3(-10.0, -10.0, 10.0),
            glm.vec3( 10.0, -10.0, 10.0),
        ]

        self.lightColors = [
            glm.vec3(300.0, 300.0, 300.0),
            glm.vec3(300.0, 300.0, 300.0),
            glm.vec3(300.0, 300.0, 300.0),
            glm.vec3(300.0, 300.0, 300.0)
        ]

        self.nrRows    = 7
        self.nrColumns = 7
        self.spacing = 2.5

        # initialize static shader uniforms before rendering
        # --------------------------------------------------
        projection = glm.perspective(glm.radians(self.camera.zoom), float(self.width / self.height), 0.1, 100.0)
        self.shader.use()
        self.shader.setUniformMatrix4fv("projection", projection)

    def cleanup(self) -> None:
        pass

    def render(self) -> None:
        super().render()
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.shader.use()
        view = self.camera.GetViewMatrix()
        self.shader.setUniformMatrix4fv("view", view)
        self.shader.setUniform3fv("camPos", self.camera.position)

        # render rows*column number of spheres with varying metallic/roughness values scaled by rows and columns respectively
        model = glm.mat4(1.0)
        for row in range(self.nrRows):
            self.shader.setUniform1f("metallic", row / self.nrRows)
            for col in range(self.nrColumns): 
                # we clamp the roughness to 0.05 - 1.0 as perfectly smooth surfaces (roughness of 0.0) tend to look a bit off
                # on direct lighting.
                self.shader.setUniform1f("roughness", glm.clamp(col / self.nrColumns, 0.05, 1.0))
                model = glm.mat4(1.0)
                model = glm.translate(model, glm.vec3(
                    (col - (self.nrColumns / 2)) * self.spacing, 
                    (row - (self.nrRows / 2)) * self.spacing, 
                    0.0
                ))
                self.shader.setUniformMatrix4fv("model", model)
                #self.shader.setMat3("normalMatrix", glm.value_ptr(glm.transpose(glm.inverse(glm.mat3(model)))))
                self.renderSphere()

        # render light source (simply re-render sphere at light positions)
        # this looks a bit off as we use the same shader, but it'll make their positions obvious and 
        # keeps the codeprint small.
        for i in range(len(self.lightPositions)):
            newPos = self.lightPositions[i] + glm.vec3(glfw.get_time() * 5.0) * 5.0, 0.0, 0.0
            newPos = self.lightPositions[i]
            self.shader.setUniform3fv("lightPositions[" + str(i) + "]", newPos)
            self.shader.setUniform3fv("lightColors[" + str(i) + "]", self.lightColors[i])

            model = glm.mat4(1.0)
            model = glm.translate(model, newPos)
            model = glm.scale(model, glm.vec3(0.5))
            self.shader.setUniformMatrix4fv("model", model)
            self.renderSphere()



    def renderSphere(self) -> None:
        self.sphereVAO.bind()
        glDrawElements(GL_TRIANGLE_STRIP, self.indexCount, GL_UNSIGNED_INT, None)


if __name__ == "__main__":
    app = App()
    win = Lighting(title="Hello, Lighing!")
    app.run(win)