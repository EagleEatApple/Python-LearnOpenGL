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

class IBLIrradianceConversion(CameraWindow):

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

        # configure global opengl state
        # -----------------------------
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL) # set depth function to less than AND equal for skybox depth trick.

        # build and compile shaders
        # -------------------------
        self.pbrShader = ProgramVF("shaders/6/2.1.1.pbr.vs",
                                   "shaders/6/2.1.1.pbr.fs")
        self.equirectangularToCubemapShader = ProgramVF("shaders/6/2.1.1.cubemap.vs",
                                                        "shaders/6/2.1.1.equirectangular_to_cubemap.fs")
        self.backgroundShader = ProgramVF("shaders/6/2.1.1.background.vs",
                                          "shaders/6/2.1.1.background.fs")
        self.pbrShader.use()
        self.pbrShader.setUniform3f("albedo", 0.5, 0.0, 0.0)
        self.pbrShader.setUniform1f("ao", 1.0)

        self.backgroundShader.use()
        self.backgroundShader.setUniform1i("environmentMap", 0)


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

        self.nrRows = 7
        self.nrColumns = 7
        self.spacing = 2.5

        # pbr: setup framebuffer
        # ----------------------
        self.captureFBO = Framebuffer()
        self.captureRBO = Renderbuffer(GL_DEPTH_COMPONENT32, 512, 512)
        self.captureFBO.attachRenderbuffer(
            GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.captureRBO)

        # pbr: load the HDR environment map
        # ---------------------------------
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
        self.envCubemap.setFiltering(GL_LINEAR, GL_LINEAR)
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
        self.equirectangularToCubemapShader.setUniformMatrix4fv(
            "projection", captureProjection)
        hdrTexture.bind(0)

        # don't forget to configure the viewport to the capture dimensions.
        glViewport(0, 0, 512, 512)
        self.captureFBO.bind()
        for i in range(6):
            self.equirectangularToCubemapShader.setUniformMatrix4fv("view", captureViews[i])
            self.captureFBO.setTextureLayer(GL_COLOR_ATTACHMENT0, self.envCubemap.tex_id, 0, i)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.renderCube()
        glBindFramebuffer(GL_FRAMEBUFFER, 0)


        # initialize static shader uniforms before rendering
        # --------------------------------------------------
        projection = glm.perspective(glm.radians(self.camera.zoom), self.width / self.height, 0.1, 100.0)
        self.pbrShader.use()
        self.pbrShader.setUniformMatrix4fv("projection", projection)
        self.backgroundShader.use()
        self.backgroundShader.setUniformMatrix4fv("projection", projection)

        glViewport(0, 0, self.width, self.height)

    def cleanup(self) -> None:
        pass

    def render(self) -> None:
        super().render()
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.pbrShader.use()
        view = self.camera.GetViewMatrix()
        self.pbrShader.setUniformMatrix4fv("view", view)
        self.pbrShader.setUniform3fv("camPos", self.camera.position)

        # render rows*column number of spheres with varying metallic/roughness values scaled by rows and columns respectively
        model = glm.mat4(1.0)
        for row in range(self.nrRows):
            self.pbrShader.setUniform1f("metallic", row / self.nrRows)
            for col in range(self.nrColumns):
                # we clamp the roughness to 0.025 - 1.0 as perfectly smooth surfaces (roughness of 0.0) tend to look a bit off
                # on direct lighting.
                self.pbrShader.setUniform1f("roughness", glm.clamp(col / self.nrColumns, 0.05, 1.0))
                model = glm.mat4(1.0)
                model = glm.translate(model, glm.vec3(
                    (col - (self.nrColumns / 2)) * self.spacing,
                    (row - (self.nrRows / 2)) * self.spacing,
                    -2.0
                ))
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


if __name__ == "__main__":
    app = App()
    win = IBLIrradianceConversion(title="Hello, IBL!")
    app.run(win)