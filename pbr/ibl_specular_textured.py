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


class IBLSpecularTextured(CameraWindow):
    def init(self) -> None:
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
            if (not oddRow):  # even rows: y == 0, y == 2 and so on
                for x in range(X_SEGMENTS + 1):
                    indices.append(y * (X_SEGMENTS + 1) + x)
                    indices.append((y + 1) * (X_SEGMENTS + 1) + x)
            else:
                for x in range(X_SEGMENTS, -1, -1):
                    indices.append((y + 1) * (X_SEGMENTS + 1) + x)
                    indices.append(y * (X_SEGMENTS + 1) + x)

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
        attribute_aNormal = VertexAttribute(
            "aNormal", 1, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat))
        attribute_aTexCoords = VertexAttribute(
            "aTexCoords", 2, 2, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat))
        self.sphereVAO.setVertexBuffer(vbo, 0, 0, 8 * sizeof(GLfloat))
        self.sphereVAO.setVertexAttribute(0, attribute_aPos)
        self.sphereVAO.setVertexAttribute(0, attribute_aNormal)
        self.sphereVAO.setVertexAttribute(0, attribute_aTexCoords)
        self.sphereVAO.setElementBuffer(ebo)

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
        glDepthFunc(GL_LEQUAL) # set depth function to less than AND equal for skybox depth trick.
        #enable seamless cubemap sampling for lower mip levels in the pre-filter map.
        glEnable(GL_TEXTURE_CUBE_MAP_SEAMLESS)

        # build and compile shaders
        # -------------------------
        self.pbrShader = ProgramVF("shaders/6/2.2.2.pbr.vs",
                                   "shaders/6/2.2.2.pbr.fs")
        self.equirectangularToCubemapShader = ProgramVF("shaders/6/2.2.2.cubemap.vs",
                                                        "shaders/6/2.2.2.equirectangular_to_cubemap.fs")
        self.irradianceShader = ProgramVF("shaders/6/2.2.2.cubemap.vs",
                                          "shaders/6/2.2.2.irradiance_convolution.fs")
        self.prefilterShader = ProgramVF("shaders/6/2.2.2.cubemap.vs",
                                          "shaders/6/2.2.2.prefilter.fs")
        self.brdfShader = ProgramVF("shaders/6/2.2.2.brdf.vs",
                                   "shaders/6/2.2.2.brdf.fs")
        self.backgroundShader = ProgramVF("shaders/6/2.2.2.background.vs",
                                          "shaders/6/2.2.2.background.fs")
        
        self.pbrShader.use()
        self.pbrShader.setUniform1i("irradianceMap", 0)
        self.pbrShader.setUniform1i("prefilterMap", 1)
        self.pbrShader.setUniform1i("brdfLUT", 2)
        self.pbrShader.setUniform1i("albedoMap", 3)
        self.pbrShader.setUniform1i("normalMap", 4)
        self.pbrShader.setUniform1i("metallicMap", 5)
        self.pbrShader.setUniform1i("roughnessMap", 6)
        self.pbrShader.setUniform1i("aoMap", 7)

        self.backgroundShader.use()
        self.backgroundShader.setUniform1i("environmentMap", 0)

        # load PBR material textures
        # --------------------------
        # rusted iron
        self.ironAlbedoMap = ImageTexture2D("textures/pbr/rusted_iron/albedo.png",flip_y=True)
        self.ironNormalMap = ImageTexture2D("textures/pbr/rusted_iron/normal.png")
        self.ironMetallicMap = ImageTexture2D("textures/pbr/rusted_iron/metallic.png")
        self.ironRoughnessMap = ImageTexture2D("textures/pbr/rusted_iron/roughness.png")
        self.ironAOMap = ImageTexture2D("textures/pbr/rusted_iron/ao.png")

        # gold
        self.goldAlbedoMap = ImageTexture2D("textures/pbr/gold/albedo.png")
        self.goldNormalMap = ImageTexture2D("textures/pbr/gold/normal.png")
        self.goldMetallicMap = ImageTexture2D("textures/pbr/gold/metallic.png")
        self.goldRoughnessMap = ImageTexture2D("textures/pbr/gold/roughness.png")
        self.goldAOMap = ImageTexture2D("textures/pbr/gold/ao.png")

        # grass
        self.grassAlbedoMap = ImageTexture2D("textures/pbr/grass/albedo.png")
        self.grassNormalMap = ImageTexture2D("textures/pbr/grass/normal.png")
        self.grassMetallicMap = ImageTexture2D("textures/pbr/grass/metallic.png")
        self.grassRoughnessMap = ImageTexture2D("textures/pbr/grass/roughness.png")
        self.grassAOMap = ImageTexture2D("textures/pbr/grass/ao.png")

        # plastic
        self.plasticAlbedoMap = ImageTexture2D("textures/pbr/plastic/albedo.png")
        self.plasticNormalMap = ImageTexture2D("textures/pbr/plastic/normal.png")
        self.plasticMetallicMap = ImageTexture2D("textures/pbr/plastic/metallic.png")
        self.plasticRoughnessMap = ImageTexture2D("textures/pbr/plastic/roughness.png")
        self.plasticAOMap = ImageTexture2D("textures/pbr/plastic/ao.png")

        # wall
        self.wallAlbedoMap = ImageTexture2D("textures/pbr/wall/albedo.png")
        self.wallNormalMap = ImageTexture2D("textures/pbr/wall/normal.png")
        self.wallMetallicMap = ImageTexture2D("textures/pbr/wall/metallic.png")
        self.wallRoughnessMap = ImageTexture2D("textures/pbr/wall/roughness.png")
        self.wallAOMap = ImageTexture2D("textures/pbr/wall/ao.png")

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

        # pbr: setup framebuffer
        # ----------------------
        self.captureFBO = Framebuffer()
        self.captureRBO = Renderbuffer(GL_DEPTH_COMPONENT24, 512, 512)
        self.captureFBO.attachRenderbuffer(
            GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.captureRBO)

        # pbr: load the HDR environment map
        # ---------------------------------
        hdrTexture = 0
        try:
            hdrTexture = HDRImageTexture2D("textures/hdr/newport_loft.hdr", True)
            hdrTexture.setFiltering(GL_LINEAR, GL_LINEAR)
            hdrTexture.setWrapMode(GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE)

        except:
            print("Failed to load HDR image.")
            return

        # pbr: setup cubemap to render to and attach to framebuffer
        # ---------------------------------------------------------
        self.envCubemap = TextureCubemap(GL_RGB16F, 512, 512)
        self.envCubemap.setFiltering(GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR)
        self.envCubemap.setWrapMode(GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE)

        # pbr: set up projection and view matrices for capturing data onto the 6 cubemap face directions
        # ----------------------------------------------------------------------------------------------
        captureProjection = glm.perspective(glm.radians(90.0), 1.0, 0.1, 10.0)
        captureViews = [
            glm.lookAt(glm.vec3(0.0, 0.0, 0.0), glm.vec3( 1.0,  0.0,  0.0), glm.vec3(0.0, -1.0,  0.0)),
            glm.lookAt(glm.vec3(0.0, 0.0, 0.0), glm.vec3(-1.0,  0.0,  0.0), glm.vec3(0.0, -1.0,  0.0)),
            glm.lookAt(glm.vec3(0.0, 0.0, 0.0), glm.vec3( 0.0,  1.0,  0.0), glm.vec3(0.0,  0.0,  1.0)),
            glm.lookAt(glm.vec3(0.0, 0.0, 0.0), glm.vec3( 0.0, -1.0,  0.0), glm.vec3(0.0,  0.0, -1.0)),
            glm.lookAt(glm.vec3(0.0, 0.0, 0.0), glm.vec3( 0.0,  0.0,  1.0), glm.vec3(0.0, -1.0,  0.0)),
            glm.lookAt(glm.vec3(0.0, 0.0, 0.0), glm.vec3( 0.0,  0.0, -1.0), glm.vec3(0.0, -1.0,  0.0))
        ]

        # pbr: convert HDR equirectangular environment map to cubemap equivalent
        # ----------------------------------------------------------------------
        self.equirectangularToCubemapShader.use()
        self.equirectangularToCubemapShader.setUniform1i("equirectangularMap", 0)
        self.equirectangularToCubemapShader.setUniformMatrix4fv("projection", captureProjection)
        
        hdrTexture.bind(0)

        glViewport(0, 0, 512, 512) # don't forget to configure the viewport to the capture dimensions.
        self.captureFBO.bind()
        for i in range(6):

            self.equirectangularToCubemapShader.setUniformMatrix4fv("view", captureViews[i])
            self.captureFBO.setTextureLayer(GL_COLOR_ATTACHMENT0, self.envCubemap.tex_id, 0, i)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.renderCube()

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # then let OpenGL generate mipmaps from first mip face (combatting visible dots artifact)
        self.envCubemap.generateMipmap()

        # pbr: create an irradiance cubemap, and re-scale capture FBO to irradiance scale.
        # --------------------------------------------------------------------------------
        self.irradianceMap = TextureCubemap(GL_RGB16F, 32, 32)
        self.irradianceMap.setFiltering(GL_LINEAR, GL_LINEAR)
        self.irradianceMap.setWrapMode(GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE)

        self.captureFBO.bind()
        self.captureRBO.bind()
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, 32, 32)

        # pbr: solve diffuse integral by convolution to create an irradiance (cube)map.
        # -----------------------------------------------------------------------------
        self.irradianceShader.use()
        self.irradianceShader.setUniform1i("environmentMap", 0)
        self.irradianceShader.setUniformMatrix4fv("projection", captureProjection)
        self.envCubemap.bind(0)

        glViewport(0, 0, 32, 32) # don't forget to configure the viewport to the capture dimensions.
        self.captureFBO.bind()
        for i in range(6):
            self.irradianceShader.setUniformMatrix4fv("view", captureViews[i])
            self.captureFBO.setTextureLayer(GL_COLOR_ATTACHMENT0, self.irradianceMap.tex_id, 0, i) 
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.renderCube()
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # pbr: create a pre-filter cubemap, and re-scale capture FBO to pre-filter scale.
        # --------------------------------------------------------------------------------
        maxMipLevels = 5
        self.prefilterMap = TextureCubemap(GL_RGB16F, 128, 128, maxMipLevels)
        self.prefilterMap.setFiltering(GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR)
        self.prefilterMap.setWrapMode(GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE,GL_CLAMP_TO_EDGE)
        self.prefilterMap.generateMipmap()

        # pbr: run a quasi monte-carlo simulation on the environment lighting to create a prefilter (cube)map.
        # ----------------------------------------------------------------------------------------------------
        self.prefilterShader.use()
        self.prefilterShader.setUniform1i("environmentMap", 0)
        self.prefilterShader.setUniformMatrix4fv("projection", captureProjection)
        self.envCubemap.bind(0)

        self.captureFBO.bind()
        for mip in range(maxMipLevels):
            # reisze framebuffer according to mip-level size.
            mipWidth = int(128 * pow(0.5, mip))
            mipHeight = int(128 * pow(0.5, mip))
            self.captureRBO.bind()
            self.captureRBO.setStorage(GL_DEPTH_COMPONENT24, mipWidth, mipHeight)
            glViewport(0, 0, mipWidth, mipHeight)
            roughness = mip / (maxMipLevels - 1)
            self.prefilterShader.setUniform1f("roughness", roughness)
            for i in range(6):
                self.prefilterShader.setUniformMatrix4fv("view", captureViews[i])
                self.captureFBO.setTextureLayer(GL_COLOR_ATTACHMENT0, self.prefilterMap.tex_id, mip, i)
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                self.renderCube()
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        # pbr: generate a 2D LUT from the BRDF equations used.
        # ----------------------------------------------------
        self.brdfLUTTexture = Texture2D(1, GL_RG16F, 512, 512,  GL_RG, GL_FLOAT)
        self.brdfLUTTexture.setFiltering(GL_LINEAR, GL_LINEAR)
        self.brdfLUTTexture.setWrapMode(GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE)

        # then re-configure capture framebuffer object and render screen-space quad with BRDF shader.
        self.captureFBO.bind()
        self.captureRBO.bind()
        self.captureRBO.setStorage(GL_DEPTH_COMPONENT24, 512, 512)
        self.captureFBO.attachTexture2D(GL_COLOR_ATTACHMENT0, self.brdfLUTTexture, 0)

        glViewport(0, 0, 512, 512)
        self.brdfShader.use()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.renderQuad()

        glBindFramebuffer(GL_FRAMEBUFFER, 0)


        # initialize static shader uniforms before rendering
        # --------------------------------------------------
        projection = glm.perspective(glm.radians(self.camera.zoom), self.width / self.height, 0.1, 100.0)
        self.pbrShader.use()
        self.pbrShader.setUniformMatrix4fv("projection", projection)
        self.backgroundShader.use()
        self.backgroundShader.setUniformMatrix4fv("projection", projection)

        # then before rendering, configure the viewport to the original framebuffer's screen dimensions

        glViewport(0, 0, self.width, self.height)

    def cleanup(self) -> None:
        pass

    def render(self) -> None:
        super().render()
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


        # render scene, supplying the convoluted irradiance map to the final shader.
        # ------------------------------------------------------------------------------------------
        self.pbrShader.use()
        model = glm.mat4(1.0)
        view = self.camera.GetViewMatrix()
        self.pbrShader.setUniformMatrix4fv("view", view)
        self.pbrShader.setUniform3fv("camPos", self.camera.position)

        # bind pre-computed IBL data
        self.irradianceMap.bind(0)
        self.prefilterMap.bind(1)
        self.brdfLUTTexture.bind(2)

        # rusted iron
        self.ironAlbedoMap.bind(3)
        self.ironNormalMap.bind(4)
        self.ironMetallicMap.bind(5)
        self.ironRoughnessMap.bind(6)
        self.ironAOMap.bind(7)

        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(-5.0, 0.0, 2.0))
        self.pbrShader.setUniformMatrix4fv("model", model)
        self.renderSphere()

        # gold
        self.goldAlbedoMap.bind(3)
        self.goldNormalMap.bind(4)
        self.goldMetallicMap.bind(5)
        self.goldRoughnessMap.bind(6)
        self.goldAOMap.bind(7)


        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(-3.0, 0.0, 2.0))
        self.pbrShader.setUniformMatrix4fv("model", model)
        self.renderSphere()

        # grass
        self.grassAlbedoMap.bind(3)
        self.grassNormalMap.bind(4)
        self.grassMetallicMap.bind(5)
        self.grassRoughnessMap.bind(6)
        self.grassAOMap.bind(7)

        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(-1.0, 0.0, 2.0))
        self.pbrShader.setUniformMatrix4fv("model", model)
        self.renderSphere()

        # plastic
        self.plasticAlbedoMap.bind(3)
        self.plasticNormalMap.bind(4)
        self.plasticMetallicMap.bind(5)
        self.plasticRoughnessMap.bind(6)
        self.plasticAOMap.bind(7)

        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(1.0, 0.0, 2.0))
        self.pbrShader.setUniformMatrix4fv("model", model)
        self.renderSphere()

        # wall
        self.wallAlbedoMap.bind(3)
        self.wallNormalMap.bind(4)
        self.wallMetallicMap.bind(5)
        self.wallRoughnessMap.bind(6)
        self.wallAOMap.bind(7)

        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(3.0, 0.0, 2.0))
        self.pbrShader.setUniformMatrix4fv("model", model)
        self.renderSphere()

        # render light source (simply re-render sphere at light positions)
        # this looks a bit off as we use the same shader, but it'll make their positions obvious and 
        # keeps the codeprint small.
        for i in range(len(self.lightPositions)):

            newPos = self.lightPositions[i] + glm.vec3(glm.sin(glfw.get_time() * 5.0) * 5.0, 0.0, 0.0)
            newPos = self.lightPositions[i]
            self.pbrShader.setUniform3fv("lightPositions[" + str(i) + "]", newPos)
            self.pbrShader.setUniform3fv("lightColors[" + str(i) + "]", self.lightColors[i])

            model = glm.mat4(1.0)
            model = glm.translate(model, newPos)
            model = glm.scale(model, glm.vec3(0.5))
            self.pbrShader.setUniformMatrix4fv("model", model)
            self.renderSphere()

        # render skybox (render as last to prevent overdraw)
        self.backgroundShader.use()
        self.backgroundShader.setUniformMatrix4fv("view", view)
        self.envCubemap.bind(0)
        self.renderCube()

    def renderCube(self) -> None:
        self.cubeVAO.bind()
        glDrawArrays(GL_TRIANGLES, 0, 36)

    def renderSphere(self) -> None:
        self.sphereVAO.bind()
        glDrawElements(GL_TRIANGLE_STRIP, self.indexCount,
                       GL_UNSIGNED_INT, None)

    def renderQuad(self) -> None:
        self.quadVAO.bind()
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

if __name__ == "__main__":
    app = App()
    win = IBLSpecularTextured(1280, 720, "Hello, IBL!")
    app.run(win)