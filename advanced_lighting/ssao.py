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

def lerp(a : float, b : float, f : float) -> float:
    return a + f * (b - a)

class SSAO(CameraWindow):


    def init(self) -> None:
        self.camera.position = glm.vec3(0.0, 0.0, 5.0)
        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)

        # build and compile shaders
        # ------------------------------------
        self.shaderGeometryPass = ProgramVF("shaders/5/9.ssao_geometry.vs",
                                            "shaders/5/9.ssao_geometry.fs")
        self.shaderLightingPass = ProgramVF("shaders/5/9.ssao.vs",
                                            "shaders/5/9.ssao_lighting.fs")
        self.shaderSSAO = ProgramVF("shaders/5/9.ssao.vs",
                                        "shaders/5/9.ssao.fs")
        self.shaderSSAOBlur = ProgramVF("shaders/5/9.ssao.vs",
                                        "shaders/5/9.ssao_blur.fs")

        # load models
        self.backpack = Model("objects/backpack/backpack.obj")
       
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

        # setup cube VAO
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

        # configure g-buffer framebuffer
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
        self.gAlbedo = Texture2D(1, GL_RGBA8, self.width, self.height, GL_RGBA, GL_UNSIGNED_BYTE)
        self.gAlbedo.setFiltering(GL_NEAREST, GL_NEAREST)
        self.gBuffer.attachTexture2D(GL_COLOR_ATTACHMENT2, self.gAlbedo, 0)
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

        # also create framebuffer to hold SSAO processing stage 
        # -----------------------------------------------------
        self.ssaoFBO = Framebuffer()
        self.ssaoFBO.bind()
        # SSAO color buffer
        self.ssaoColorBuffer = Texture2D(1, GL_R8, self.width, self.height, GL_RED, GL_FLOAT)
        self.ssaoColorBuffer.setFiltering(GL_NEAREST, GL_NEAREST)
        self.ssaoFBO.attachTexture2D(GL_COLOR_ATTACHMENT0, self.ssaoColorBuffer, 0)
        if self.ssaoFBO.isComplete() is not True:
            raise RuntimeError('Framebuffer not complete!')        
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        # and blur stage
        self.ssaoBlurFBO = Framebuffer()
        self.ssaoBlurFBO.bind()
        self.ssaoColorBufferBlur = Texture2D(1, GL_R8, self.width, self.height, GL_RED, GL_FLOAT)
        self.ssaoColorBufferBlur.setFiltering(GL_NEAREST, GL_NEAREST)
        self.ssaoBlurFBO.attachTexture2D(GL_COLOR_ATTACHMENT0, self.ssaoColorBufferBlur, 0)
        if self.ssaoBlurFBO.isComplete() is not True:
            raise RuntimeError('Framebuffer not complete!')  
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # generate sample kernel
        # ----------------------
        self.ssaoKernel = []
        for i in range(64):
            sample = glm.vec3(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(0, 1))
            sample = glm.normalize(sample)
            sample *= random.uniform(0, 1)
            scale = float(i) / 64.0

            # scale samples s.t. they're more aligned to center of kernel
            scale = lerp(0.1, 1.0, scale * scale)
            sample *= scale
            self.ssaoKernel.append(sample)

        # generate noise texture
        # ----------------------
        ssaoNoise = []
        for i in range(16):
            noise = (random.uniform(-1, 1), random.uniform(-1, 1), 0.0) # rotate around z-axis (in tangent space)
            ssaoNoise.append(noise)

        ssaoNoiseArr = np.array(ssaoNoise, dtype= float)
        self.noiseTexture = Texture2D(1, GL_RGB32F, 4, 4, GL_RGB, GL_FLOAT, ssaoNoiseArr)
        self.noiseTexture.setFiltering(GL_NEAREST, GL_NEAREST)
        self.noiseTexture.setWrapMode(GL_REPEAT, GL_REPEAT)
        
        # lighting info
        # -------------
        self.lightPos = glm.vec3(2.0, 4.0, -2.0)
        self.lightColor = glm.vec3(0.2, 0.2, 0.7)

        # shader configuration
        # --------------------
        self.shaderLightingPass.use()
        self.shaderLightingPass.setUniform1i("gPosition", 0)
        self.shaderLightingPass.setUniform1i("gNormal", 1)
        self.shaderLightingPass.setUniform1i("gAlbedo", 2)
        self.shaderLightingPass.setUniform1i("ssao", 3)
        self.shaderSSAO.use()
        self.shaderSSAO.setUniform1i("gPosition", 0)
        self.shaderSSAO.setUniform1i("gNormal", 1)
        self.shaderSSAO.setUniform1i("texNoise", 2)
        self.shaderSSAOBlur.use()
        self.shaderSSAOBlur.setUniform1i("ssaoInput", 0)

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
        projection = glm.perspective(glm.radians(self.camera.zoom), float(self.width / self.height), 0.1, 50.0)
        view = self.camera.GetViewMatrix()
        model = glm.mat4(1.0)
        self.shaderGeometryPass.use()
        self.shaderGeometryPass.setUniformMatrix4fv("projection", projection)
        self.shaderGeometryPass.setUniformMatrix4fv("view", view)
        # room cube
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(0.0, 7.0, 0.0))
        model = glm.scale(model, glm.vec3(7.5, 7.5, 7.5))
        self.shaderGeometryPass.setUniformMatrix4fv("model", model)
        self.shaderGeometryPass.setUniform1i("invertedNormals", 1) # invert normals as we're inside the cube
        self.renderCube()
        self.shaderGeometryPass.setUniform1i("invertedNormals", 0) 
        # backpack model on the floor
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(0.0, 0.5, 0.0))
        model = glm.rotate(model, glm.radians(-90.0), glm.vec3(1.0, 0.0, 0.0))
        model = glm.scale(model, glm.vec3(1.0))
        self.shaderGeometryPass.setUniformMatrix4fv("model", model)
        self.backpack.Draw(self.shaderGeometryPass)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # 2. generate SSAO texture
        # ------------------------
        self.ssaoFBO.bind()
        glClear(GL_COLOR_BUFFER_BIT)
        self.shaderSSAO.use()
        # Send kernel + rotation 
        for i in range(64):
           self. shaderSSAO.setUniform3fv("samples[" + str(i) + "]", self.ssaoKernel[i])
        self.shaderSSAO.setUniformMatrix4fv("projection", projection)
        
        self.gPosition.bind(0)
        self.gNormal.bind(1)
        self.noiseTexture.bind(2)
        self.renderQuad()
        glBindFramebuffer(GL_FRAMEBUFFER, 0)


        # 3. blur SSAO texture to remove noise
        # ------------------------------------
        self.ssaoBlurFBO.bind()
        glClear(GL_COLOR_BUFFER_BIT)
        self.shaderSSAOBlur.use()
        self.ssaoColorBuffer.bind(0)
        self.renderQuad()
        glBindFramebuffer(GL_FRAMEBUFFER, 0)


        # 4. lighting pass: traditional deferred Blinn-Phong lighting with added screen-space ambient occlusion
        # -----------------------------------------------------------------------------------------------------
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.shaderLightingPass.use()
        # send light relevant uniforms
        lightPosView = glm.vec3(self.camera.GetViewMatrix() * glm.vec4(self.lightPos, 1.0))
        self.shaderLightingPass.setUniform3fv("light.Position", lightPosView)
        self.shaderLightingPass.setUniform3fv("light.Color", self.lightColor)
        # Update attenuation parameters
        linear    = 0.09
        quadratic = 0.032
        self.shaderLightingPass.setUniform1f("light.Linear", linear)
        self.shaderLightingPass.setUniform1f("light.Quadratic", quadratic)
        self.gPosition.bind(0)
        self.gNormal.bind(1)
        self.gAlbedo.bind(2)
        self.ssaoColorBufferBlur.bind(3)
        self.renderQuad()


    def renderCube(self) -> None:
        self.cubeVAO.bind()
        glDrawArrays(GL_TRIANGLES, 0, 36)

    def renderQuad(self) -> None:
        self.quadVAO.bind()
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)


if __name__ == "__main__":
    app = App()
    win = SSAO(title="Hello, SSAO!")
    app.run(win)