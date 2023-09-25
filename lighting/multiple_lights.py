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

class MultipleLights(CameraWindow):


    def init(self) -> None:
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)

        # build and compile shader
        # ------------------------------------
        self.lightingShader = ProgramVF(
            "shaders/2/6.multiple_lights.vs", "shaders/2/6.multiple_lights.fs")
        self.lightCubeShader = ProgramVF(
            "shaders/2/6.light_cube.vs", "shaders/2/6.light_cube.fs")
        
        # set up vertex data (and buffer(s)) and configure vertex attributes
        # ------------------------------------------------------------------
        self.vertices = np.array([
            #  positions            normals      texture coords
            -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  0.0,  0.0,
            0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  1.0,  0.0,
            0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  1.0,  1.0,
            0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  1.0,  1.0,
            -0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  0.0,  1.0,
            -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  0.0,  0.0,

            -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  0.0,  0.0,
            0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  1.0,  0.0,
            0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  1.0,  1.0,
            0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  1.0,  1.0,
            -0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  0.0,  1.0,
            -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  0.0,  0.0,

            -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,  1.0,  0.0,
            -0.5,  0.5, -0.5, -1.0,  0.0,  0.0,  1.0,  1.0,
            -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,  0.0,  1.0,
            -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,  0.0,  1.0,
            -0.5, -0.5,  0.5, -1.0,  0.0,  0.0,  0.0,  0.0,
            -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,  1.0,  0.0,

            0.5,  0.5,  0.5,  1.0,  0.0,  0.0,  1.0,  0.0,
            0.5,  0.5, -0.5,  1.0,  0.0,  0.0,  1.0,  1.0,
            0.5, -0.5, -0.5,  1.0,  0.0,  0.0,  0.0,  1.0,
            0.5, -0.5, -0.5,  1.0,  0.0,  0.0,  0.0,  1.0,
            0.5, -0.5,  0.5,  1.0,  0.0,  0.0,  0.0,  0.0,
            0.5,  0.5,  0.5,  1.0,  0.0,  0.0,  1.0,  0.0,

            -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  0.0,  1.0,
            0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  1.0,  1.0,
            0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  1.0,  0.0,
            0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  1.0,  0.0,
            -0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  0.0,  0.0,
            -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  0.0,  1.0,

            -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  0.0,  1.0,
            0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  1.0,  1.0,
            0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  1.0,  0.0,
            0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  1.0,  0.0,
            -0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  0.0,  0.0,
            -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  0.0,  1.0
        ], dtype=GLfloat)
        # positions all containers
        self.cubePositions = [
            glm.vec3(0.0,  0.0,  0.0),
            glm.vec3(2.0,  5.0, -15.0),
            glm.vec3(-1.5, -2.2, -2.5),
            glm.vec3(-3.8, -2.0, -12.3),
            glm.vec3(2.4, -0.4, -3.5),
            glm.vec3(-1.7,  3.0, -7.5),
            glm.vec3(1.3, -2.0, -2.5),
            glm.vec3(1.5,  2.0, -2.5),
            glm.vec3(1.5,  0.2, -1.5),
            glm.vec3(-1.3,  1.0, -1.5)
        ]
        # positions of the point lights
        self.pointLightPositions = [
            glm.vec3(0.7,  0.2,  2.0),
            glm.vec3(2.3, -3.3, -4.0),
            glm.vec3(-4.0,  2.0, -12.0),
            glm.vec3(0.0,  0.0, -3.0)
        ]
        # first, configure the cube's VAO (and VBO)
        self.cubeVAO = VertexArrayObject()
        self.VBO = VertexBufferObject(self.vertices)
        attribute_aPos = VertexAttribute("aPos", 0, 3, GL_FLOAT, GL_FALSE, 0)
        attribute_aNormal = VertexAttribute(
            "aNormal", 1, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat))
        attribute_aTexCoords = VertexAttribute(
            "aTexCoords", 2, 2, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat))
        self.cubeVAO.setVertexBuffer(self.VBO, 0, 0, 8 * sizeof(GLfloat))
        self.cubeVAO.setVertexAttribute(0, attribute_aPos)
        self.cubeVAO.setVertexAttribute(0, attribute_aNormal)
        self.cubeVAO.setVertexAttribute(0, attribute_aTexCoords)

        # second, configure the light's VAO (VBO stays the same; the vertices are the same for the light object which is also a 3D cube)
        self.lightCubeVAO = VertexArrayObject()
        self.lightCubeVAO.setVertexBuffer(self.VBO, 0, 0, 8 * sizeof(GLfloat))
        self.lightCubeVAO.setVertexAttribute(0, attribute_aPos)

        # load textures
        #  -----------------------------------------------------------------------------
        self.diffuseMap = ImageTexture2D("textures/container2.png")
        self.specularMap = ImageTexture2D("textures/container2_specular.png")

        # shader configuration
        # --------------------
        self.lightingShader.use()
        self.lightingShader.setUniform1i("material.diffuse", 0)
        self.lightingShader.setUniform1i("material.specular", 1)

    def cleanup(self) -> None:
        self.cubeVAO.delete()
        self.lightCubeVAO.delete()
        self.VBO.delete()
        self.diffuseMap.delete()
        self.specularMap.delete()
        self.lightCubeShader.delete()
        self.lightingShader.delete()

    def render(self) -> None:
        super().render()
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # be sure to activate shader when setting uniforms/drawing objects
        self.lightingShader.use()
        self.lightingShader.setUniform3fv("viewPos", self.camera.position)
        self.lightingShader.setUniform1f("material.shininess", 32.0)

        '''
            Here we set all the uniforms for the 5/6 types of lights we have. We have to set them manually and index 
            the proper PointLight struct in the array to set each uniform variable. This can be done more code-friendly
            by defining light types as classes and set their values in there, or by using a more efficient uniform approach
            by using 'Uniform buffer objects', but that is something we'll discuss in the 'Advanced GLSL' tutorial.
        '''

        # directional light
        self.lightingShader.setUniform3f("dirLight.direction", 
            -0.2, -1.0, -0.3)
        self.lightingShader.setUniform3f("dirLight.ambient", 
            0.05, 0.05, 0.05)
        self.lightingShader.setUniform3f("dirLight.diffuse", 
            0.4, 0.4, 0.4)
        self.lightingShader.setUniform3f("dirLight.specular", 
            0.5, 0.5, 0.5)

        # point light 1
        self.lightingShader.setUniform3fv("pointLights[0].position", 
            self.pointLightPositions[0])
        self.lightingShader.setUniform3f("pointLights[0].ambient", 
            0.05, 0.05, 0.05)
        self.lightingShader.setUniform3f("pointLights[0].diffuse", 
            0.8, 0.8, 0.8)
        self.lightingShader.setUniform3f("pointLights[0].specular", 
            1.0, 1.0, 1.0)
        self.lightingShader.setUniform1f("pointLights[0].constant", 1.0)
        self.lightingShader.setUniform1f("pointLights[0].linear", 0.09)
        self.lightingShader.setUniform1f("pointLights[0].quadratic", 
            0.032)
        # point light 2
        self.lightingShader.setUniform3fv("pointLights[1].position", 
            self.pointLightPositions[1])
        self.lightingShader.setUniform3f("pointLights[1].ambient", 
            0.05, 0.05, 0.05)
        self.lightingShader.setUniform3f("pointLights[1].diffuse", 
            0.8, 0.8, 0.8)
        self.lightingShader.setUniform3f("pointLights[1].specular", 
            1.0, 1.0, 1.0)
        self.lightingShader.setUniform1f("pointLights[1].constant", 1.0)
        self.lightingShader.setUniform1f("pointLights[1].linear", 0.09)
        self.lightingShader.setUniform1f("pointLights[1].quadratic", 
            0.032)
        # point light 3
        self.lightingShader.setUniform3fv("pointLights[2].position", 
            self.pointLightPositions[2])
        self.lightingShader.setUniform3f("pointLights[2].ambient", 
            0.05, 0.05, 0.05)
        self.lightingShader.setUniform3f("pointLights[2].diffuse", 
            0.8, 0.8, 0.8)
        self.lightingShader.setUniform3f("pointLights[2].specular", 
            1.0, 1.0, 1.0)
        self.lightingShader.setUniform1f("pointLights[2].constant", 1.0)
        self.lightingShader.setUniform1f("pointLights[2].linear", 0.09)
        self.lightingShader.setUniform1f("pointLights[2].quadratic", 
            0.032)
        # point light 4
        self.lightingShader.setUniform3fv("pointLights[3].position", 
            self.pointLightPositions[3])
        self.lightingShader.setUniform3f("pointLights[3].ambient", 
            0.05, 0.05, 0.05)
        self.lightingShader.setUniform3f("pointLights[3].diffuse", 
            0.8, 0.8, 0.8)
        self.lightingShader.setUniform3f("pointLights[3].specular", 
            1.0, 1.0, 1.0)
        self.lightingShader.setUniform1f("pointLights[3].constant", 1.0)
        self.lightingShader.setUniform1f("pointLights[3].linear", 0.09)
        self.lightingShader.setUniform1f("pointLights[3].quadratic", 
            0.032)
        # spotLight
        self.lightingShader.setUniform3fv("spotLight.position", 
            self.camera.position)
        self.lightingShader.setUniform3fv("spotLight.direction", 
            self.camera.front)
        self.lightingShader.setUniform3f("spotLight.ambient", 
            0.0, 0.0, 0.0)
        self.lightingShader.setUniform3f("spotLight.diffuse", 
            1.0, 1.0, 1.0)
        self.lightingShader.setUniform3f("spotLight.specular", 
            1.0, 1.0, 1.0)
        self.lightingShader.setUniform1f("spotLight.constant", 1.0)
        self.lightingShader.setUniform1f("spotLight.linear", 0.09)
        self.lightingShader.setUniform1f("spotLight.quadratic", 0.032)
        self.lightingShader.setUniform1f("spotLight.cutOff", 
            glm.cos(glm.radians(12.5)))
        self.lightingShader.setUniform1f("spotLight.outerCutOff", 
            glm.cos(glm.radians(15.0)))

        # view/projection transformations
        projection = glm.perspective(
            glm.radians(self.camera.zoom), float(self.width/self.height), 0.1, 100.0)
        view = self.camera.GetViewMatrix()
        self.lightingShader.setUniformMatrix4fv("projection", projection)
        self.lightingShader.setUniformMatrix4fv("view", view)

        # world transformation
        model = glm.mat4(1.0)
        self.lightingShader.setUniformMatrix4fv("model", model)

        # bind diffuse map
        # 
        self.diffuseMap.bind(0)
        # 
        self.specularMap.bind(1)

        # render containers
        self.cubeVAO.bind()
        for i in range(0, 10):
            model = glm.mat4(1.0)
            model = glm.translate(model, self.cubePositions[i])
            angle = 20.0 * i
            model = glm.rotate(model, glm.radians(
                angle), glm.vec3(1.0, 0.3, 0.5))
            self.lightingShader.setUniformMatrix4fv("model", model)
            glDrawArrays(GL_TRIANGLES, 0, 36)

        # also draw the lamp object
        self.lightCubeShader.use()
        self.lightCubeShader.setUniformMatrix4fv("projection", projection)
        self.lightCubeShader.setUniformMatrix4fv("view", view)

        # we now draw as many light bulbs as we have point lights.
        self.lightCubeVAO.bind()
        for i in range(0, 4):
            model = glm.mat4(1.0)
            model = glm.translate(model, self.pointLightPositions[i])
            model = glm.scale(model, glm.vec3(0.2))
            self.lightCubeShader.setUniformMatrix4fv("model", model)
            glDrawArrays(GL_TRIANGLES, 0, 36)

if __name__ == "__main__":
    app = App()
    win = MultipleLights(title="Hello, Light!")
    app.run(win)
