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
from learnopengl import *

class DeferredShading(CameraWindow):


    def init(self) -> None:
        self.camera.position = glm.vec3(0.0, 0.0, 5.0)

        self.cubeVertices = np.array([
            # back face
            -1.0, -1.0, -1.0,  0.0,  0.0, -1.0, 0.0, 0.0,  # bottom-left
            1.0,  1.0, -1.0,  0.0,  0.0, -1.0, 1.0, 1.0,  # top-right
            1.0, -1.0, -1.0,  0.0,  0.0, -1.0, 1.0, 0.0,  # bottom-right
            1.0,  1.0, -1.0,  0.0,  0.0, -1.0, 1.0, 1.0,  # top-right
            -1.0, -1.0, -1.0,  0.0,  0.0, -1.0, 0.0, 0.0,  # bottom-left
            -1.0,  1.0, -1.0,  0.0,  0.0, -1.0, 0.0, 1.0,  # top-left
            # front face
            -1.0, -1.0,  1.0,  0.0,  0.0,  1.0, 0.0, 0.0,  # bottom-left
            1.0, -1.0,  1.0,  0.0,  0.0,  1.0, 1.0, 0.0,  # bottom-right
            1.0,  1.0,  1.0,  0.0,  0.0,  1.0, 1.0, 1.0,  # top-right
            1.0,  1.0,  1.0,  0.0,  0.0,  1.0, 1.0, 1.0,  # top-right
            -1.0,  1.0,  1.0,  0.0,  0.0,  1.0, 0.0, 1.0,  # top-left
            -1.0, -1.0,  1.0,  0.0,  0.0,  1.0, 0.0, 0.0,  # bottom-left
            # left face
            -1.0,  1.0,  1.0, -1.0,  0.0,  0.0, 1.0, 0.0,  # top-right
            -1.0,  1.0, -1.0, -1.0,  0.0,  0.0, 1.0, 1.0,  # top-left
            -1.0, -1.0, -1.0, -1.0,  0.0,  0.0, 0.0, 1.0,  # bottom-left
            -1.0, -1.0, -1.0, -1.0,  0.0,  0.0, 0.0, 1.0,  # bottom-left
            -1.0, -1.0,  1.0, -1.0,  0.0,  0.0, 0.0, 0.0,  # bottom-right
            -1.0,  1.0,  1.0, -1.0,  0.0,  0.0, 1.0, 0.0,  # top-right
            # right face
            1.0,  1.0,  1.0,  1.0,  0.0,  0.0, 1.0, 0.0,  # top-left
            1.0, -1.0, -1.0,  1.0,  0.0,  0.0, 0.0, 1.0,  # bottom-right
            1.0,  1.0, -1.0,  1.0,  0.0,  0.0, 1.0, 1.0,  # top-right
            1.0, -1.0, -1.0,  1.0,  0.0,  0.0, 0.0, 1.0,  # bottom-right
            1.0,  1.0,  1.0,  1.0,  0.0,  0.0, 1.0, 0.0,  # top-left
            1.0, -1.0,  1.0,  1.0,  0.0,  0.0, 0.0, 0.0,  # bottom-left
            # bottom face
            -1.0, -1.0, -1.0,  0.0, -1.0,  0.0, 0.0, 1.0,  # top-right
            1.0, -1.0, -1.0,  0.0, -1.0,  0.0, 1.0, 1.0,  # top-left
            1.0, -1.0,  1.0,  0.0, -1.0,  0.0, 1.0, 0.0,  # bottom-left
            1.0, -1.0,  1.0,  0.0, -1.0,  0.0, 1.0, 0.0,  # bottom-left
            -1.0, -1.0,  1.0,  0.0, -1.0,  0.0, 0.0, 0.0,  # bottom-right
            -1.0, -1.0, -1.0,  0.0, -1.0,  0.0, 0.0, 1.0,  # top-right
            # top face
            -1.0,  1.0, -1.0,  0.0,  1.0,  0.0, 0.0, 1.0,  # top-left
            1.0,  1.0, 1.0,  0.0,  1.0,  0.0, 1.0, 0.0,  # bottom-right
            1.0,  1.0, -1.0,  0.0,  1.0,  0.0, 1.0, 1.0,  # top-right
            1.0,  1.0,  1.0,  0.0,  1.0,  0.0, 1.0, 0.0,  # bottom-right
            -1.0,  1.0, -1.0,  0.0,  1.0,  0.0, 0.0, 1.0,  # top-left
            -1.0,  1.0,  1.0,  0.0,  1.0,  0.0, 0.0, 0.0  # bottom-left
        ], dtype=GLfloat)
        self.cubeVAO = VertexArrayObject()
        self.VBO = VertexBufferObject(self.cubeVertices)
        cube_aPos = VertexAttribute("aPos", 0, 3, GL_FLOAT, GL_FALSE, 0)
        cube_aNormal = VertexAttribute(
            "aNormal", 1, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat))
        cube_aTexCoords = VertexAttribute(
            "aTexCoords", 2, 2, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat))
        self.cubeVAO.setVertexBuffer(self.VBO, 0, 0, 8 * sizeof(GLfloat))
        self.cubeVAO.setVertexAttribute(0, cube_aPos)
        self.cubeVAO.setVertexAttribute(0, cube_aNormal)
        self.cubeVAO.setVertexAttribute(0, cube_aTexCoords)


        # setup quad VAO
        self.quadVertices = np.array([
            # positions        # texture Coords
            -1.0,  1.0, 0.0, 0.0, 1.0,
            -1.0, -1.0, 0.0, 0.0, 0.0,
            1.0,  1.0, 0.0, 1.0, 1.0,
            1.0, -1.0, 0.0, 1.0, 0.0
        ], dtype=GLfloat)
        quad_aPos = VertexAttribute("aPos", 0, 3, GL_FLOAT, GL_FALSE, 0)
        quad_aTexCoord = VertexAttribute(
            "aTexCoords", 1, 2, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat))
        self.quadVAO = VertexArrayObject()
        self.quadVBO = VertexBufferObject(self.quadVertices)
        self.quadVAO.setVertexBuffer(self.quadVBO, 0, 0, 5 * sizeof(GLfloat))
        self.quadVAO.setVertexAttribute(0, quad_aPos)
        self.quadVAO.setVertexAttribute(0, quad_aTexCoord)



        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)

        # build and compile shaders
        # ------------------------------------
        self.shaderGeometryPass = ProgramVF("shaders/5/8.1.g_buffer.vs",
                                            "shaders/5/8.1.g_buffer.fs")
        self.shaderLightingPass = ProgramVF("shaders/5/8.1.deferred_shading.vs",
                                            "shaders/5/8.1.deferred_shading.fs")
        self.shaderLightBox = ProgramVF("shaders/5/8.1.deferred_light_box.vs",
                                        "shaders/5/8.1.deferred_light_box.fs")

        # load models
        self.backpack = Model("objects/backpack/backpack.obj")
        self.objectPositions = []
        self.objectPositions.append(glm.vec3(-3.0,  -0.5, -3.0))
        self.objectPositions.append(glm.vec3( 0.0,  -0.5, -3.0))
        self.objectPositions.append(glm.vec3( 3.0,  -0.5, -3.0))
        self.objectPositions.append(glm.vec3(-3.0,  -0.5,  0.0))
        self.objectPositions.append(glm.vec3( 0.0,  -0.5,  0.0))
        self.objectPositions.append(glm.vec3( 3.0,  -0.5,  0.0))
        self.objectPositions.append(glm.vec3(-3.0,  -0.5,  3.0))
        self.objectPositions.append(glm.vec3( 0.0,  -0.5,  3.0))
        self.objectPositions.append(glm.vec3( 3.0,  -0.5,  3.0))        


        # configure g-buffer framebuffer
        # ------------------------------
        self.gBuffer = Framebuffer()
        self.gBuffer.bind()
        # position color buffer
        self.gPosition = Texture2D(1, GL_RGBA16F, self.width, self.height, GL_RGBA, GL_FLOAT)
        self.gPosition.setFiltering(GL_NEAREST, GL_NEAREST)
        self.gBuffer.attachTexture2D(GL_COLOR_ATTACHMENT0, self.gPosition, 0)
        # normal color buffer
        self.gNormal = Texture2D(1, GL_RGBA16F, self.width, self.height, GL_RGBA, GL_FLOAT)
        self.gNormal.setFiltering(GL_NEAREST, GL_NEAREST)
        self.gBuffer.attachTexture2D(GL_COLOR_ATTACHMENT1, self.gNormal, 0)
        # color + specular color buffer
        self.gAlbedoSpec = Texture2D(1, GL_RGBA8, self.width, self.height, GL_RGBA, GL_UNSIGNED_BYTE)
        self.gAlbedoSpec.setFiltering(GL_NEAREST, GL_NEAREST)
        self.gBuffer.attachTexture2D(GL_COLOR_ATTACHMENT2, self.gAlbedoSpec, 0)
        # tell OpenGL which color attachments we'll use (of this framebuffer) for rendering 
        attachments = [GL_COLOR_ATTACHMENT0, GL_COLOR_ATTACHMENT1, GL_COLOR_ATTACHMENT2]
        self.gBuffer.setDrawBuffers(attachments)
        # create and attach depth buffer (renderbuffer)
        rboDepth = Renderbuffer(GL_DEPTH_COMPONENT, self.width, self.height)
        self.gBuffer.attachRenderbuffer(GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, rboDepth)
        # finally check if framebuffer is complete
        if self.gBuffer.isComplete() is not True:
            raise RuntimeError('Framebuffer not complete!')
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # lighting info
        # -------------
        NR_LIGHTS = 32
        self.lightPositions = []
        self.lightColors = []
        random.seed()
        for i in range(NR_LIGHTS):
            # calculate slightly random offsets
            xPos = random.uniform(-3, 3)
            yPos = random.uniform(-4, 2)
            zPos = random.uniform(-3, 3)
            self.lightPositions.append(glm.vec3(xPos, yPos, zPos))
            # also calculate random color
            rColor = random.uniform(0.5, 1) # between 0.5 and 1.0
            gColor = random.uniform(0.5, 1) # between 0.5 and 1.0
            bColor = random.uniform(0.5, 1) # between 0.5 and 1.0
            self.lightColors.append(glm.vec3(rColor, gColor, bColor))

        # shader configuration
        # --------------------
        self.shaderLightingPass.use()
        self.shaderLightingPass.setUniform1i("gPosition", 0)
        self.shaderLightingPass.setUniform1i("gNormal", 1)
        self.shaderLightingPass.setUniform1i("gAlbedoSpec", 2)


    def cleanup(self) -> None:
        pass


    def render(self) -> None:
        super().render()
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 1. geometry pass: render scene's geometry/color data into gbuffer
        # -----------------------------------------------------------------
        self.gBuffer.bind()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        projection = glm.perspective(glm.radians(self.camera.zoom), self.width / self.height, 0.1, 100.0)
        view = self.camera.GetViewMatrix()
        model = glm.mat4(1.0)
        self.shaderGeometryPass.use()
        self.shaderGeometryPass.setUniformMatrix4fv("projection", projection)
        self.shaderGeometryPass.setUniformMatrix4fv("view", view)
        for i in range(len(self.objectPositions)):
            model = glm.mat4(1.0)
            model = glm.translate(model, self.objectPositions[i])
            model = glm.scale(model, glm.vec3(0.5))
            self.shaderGeometryPass.setUniformMatrix4fv("model", model)
            self.backpack.Draw(self.shaderGeometryPass)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # 2. lighting pass: calculate lighting by iterating over a screen filled quad pixel-by-pixel using the gbuffer's content.
        # -----------------------------------------------------------------------------------------------------------------------
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.shaderLightingPass.use()
        self.gPosition.bind(0)
        self.gNormal.bind(1)
        self.gAlbedoSpec.bind(2)

        # send light relevant uniforms
        for i in range(len(self.lightPositions)):
            self.shaderLightingPass.setUniform3fv("lights[" + str(i) + "].Position", self.lightPositions[i])
            self.shaderLightingPass.setUniform3fv("lights[" + str(i) + "].Color", self.lightColors[i])
            # update attenuation parameters and calculate radius
            linear = 0.7
            quadratic = 1.8
            self.shaderLightingPass.setUniform1f("lights[" + str(i) + "].Linear", linear)
            self.shaderLightingPass.setUniform1f("lights[" + str(i) + "].Quadratic", quadratic)

        self.shaderLightingPass.setUniform3fv("viewPos", self.camera.position)
        # finally render quad
        self.renderQuad()

        # 2.5. copy content of geometry's depth buffer to default framebuffer's depth buffer
        # ----------------------------------------------------------------------------------
        # blit to default framebuffer. Note that this may or may not work as the internal formats of both the FBO and default framebuffer have to match.
        # the internal formats are implementation defined. This works on all of my systems, but if it doesn't on yours you'll likely have to write to the 		
        # depth buffer in another shader stage (or somehow see to match the default framebuffer's internal format with the FBO's internal format).
        glBlitNamedFramebuffer(self.gBuffer.fbo_id, 0,
            0,0,self.width,self.height,0,0,self.width, self.height, 
            GL_DEPTH_BUFFER_BIT, GL_NEAREST)
        
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # 3. render lights on top of scene
        # --------------------------------
        self.shaderLightBox.use()
        self.shaderLightBox.setUniformMatrix4fv("projection", projection)
        self.shaderLightBox.setUniformMatrix4fv("view", view)
        for i in range(len(self.lightPositions)):
            model = glm.mat4(1.0)
            model = glm.translate(model, self.lightPositions[i])
            model = glm.scale(model, glm.vec3(0.125))
            self.shaderLightBox.setUniformMatrix4fv("model", model)
            self.shaderLightBox.setUniform3fv("lightColor", self.lightColors[i])
            self.renderCube()


    def renderCube(self) -> None:
        self.cubeVAO.bind()
        glDrawArrays(GL_TRIANGLES, 0, 36)


    def renderQuad(self) -> None:
        self.quadVAO.bind()
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)



if __name__ == "__main__":
    app = App()
    win = DeferredShading(title="Hello, Deferred shading!")
    app.run(win)