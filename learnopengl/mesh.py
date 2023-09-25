from ctypes import sizeof, c_void_p

from OpenGL.GL import *
import numpy as np

from py3gl4 import *


class MeshTexture:
    def __init__(self) -> None:
        self.tex: ImageTexture2D = None
        self.type: str = ""
        self.path: str = ""


class Mesh:
    def __init__(self, vertices: np.ndarray, normals: np.ndarray,
                 texcoords: np.ndarray, tangents: np.ndarray,
                 bitangents: np.ndarray, indices: np.ndarray,
                 textures: MeshTexture) -> None:
        self.vertices = vertices
        self.normals = normals
        self.texcoords = texcoords
        self.tangents = tangents
        self.bitangents = bitangents
        self.indices = indices
        self.textures = textures
        self.setupMesh()

    # render the mesh
    def Draw(self, program: ProgramVF) -> None:
        # bind appropriate textures
        diffuseNr = 1
        specularNr = 1
        normalNr = 1
        heightNr = 1
        number_texture = len(self.textures)
        for i in range(number_texture):
            # retrieve texture number (the N in diffuse_textureN)
            number = ""
            name = self.textures[i].type
            if name == "texture_diffuse":
                number = str(diffuseNr)
                diffuseNr += 1
            elif name == "texture_specular":
                number = str(specularNr)
                specularNr += 1
            elif name == "texture_normal":
                number = str(normalNr)
                normalNr += 1
            elif name == "texture_height":
                number = str(heightNr)
                heightNr += 1
            # now set the sampler to the correct texture unit
            tex = "".join([name, number])
            program.setUniform1i(tex, i)
            self.textures[i].tex.bind(i)

        # draw mesh
        self.VAO.bind()
        glDrawElements(GL_TRIANGLES, len(self.indices),
                       GL_UNSIGNED_INT, c_void_p(0))
        

    # initializes all the buffer objects/arrays
    def setupMesh(self) -> None:
        # create buffers/arrays
        self.VAO = VertexArrayObject()
        vertices_vbo = VertexBufferObject(self.vertices)
        normals_vbo = VertexBufferObject(self.normals)
        texcoords_vbo = VertexBufferObject(self.texcoords)
        tangents_vbo = VertexBufferObject(self.tangents)
        bitangents_vbo = VertexBufferObject(self.bitangents)
        indices_ebo = ElementBufferObject(self.indices)
        attribute_aPos = VertexAttribute("aPos", 0, 3, GL_FLOAT, GL_FALSE, 0)
        attribute_aNormal = VertexAttribute(
            "aNormal", 1, 3, GL_FLOAT, GL_FALSE, 0)
        attribute_aTexCoords = VertexAttribute(
            "aTexCoords", 2, 2, GL_FLOAT, GL_FALSE, 0)
        attribute_aTangent = VertexAttribute(
            "aTangent", 3, 3, GL_FLOAT, GL_FALSE, 0)
        attribute_aBitangent = VertexAttribute(
            "aBitangent", 4, 3, GL_FLOAT, GL_FALSE, 0)
        self.VAO.setVertexBuffer(vertices_vbo, 0, 0, 3 * sizeof(GLfloat))
        self.VAO.setVertexAttribute(0, attribute_aPos)
        self.VAO.setVertexBuffer(normals_vbo, 1, 0, 3 * sizeof(GLfloat))
        self.VAO.setVertexAttribute(1, attribute_aNormal)
        self.VAO.setVertexBuffer(texcoords_vbo, 2, 0, 2 * sizeof(GLfloat))
        self.VAO.setVertexAttribute(2, attribute_aTexCoords)
        self.VAO.setVertexBuffer(tangents_vbo, 3, 0, 3 * sizeof(GLfloat))
        self.VAO.setVertexAttribute(3, attribute_aTangent)
        self.VAO.setVertexBuffer(bitangents_vbo, 4, 0, 3 * sizeof(GLfloat))
        self.VAO.setVertexAttribute(4, attribute_aBitangent)
        self.VAO.setElementBuffer(indices_ebo)
