import os
from pathlib import Path
import time

import pyassimp
import pyassimp.postprocess
import pyassimp.material
from OpenGL.GL import *
import numpy as np

from learnopengl.mesh import MeshTexture, Mesh
from py3gl4 import *


class Model:
    def __init__(self, path: str, gamma: bool = False) -> None:
        self.textures_loaded: list[MeshTexture] = []
        self.meshes: list[Mesh] = []
        self.directory: str = ""
        self.gamma_correction: bool = gamma
        self.loadModel(path)

    def Draw(self, program: ProgramVF) -> None:
        for mesh in self.meshes:
            mesh.Draw(program)

    def loadModel(self, path: str) -> None:
        # read file via ASSIMP
        scene = pyassimp.load(path)
        self.tex_path = Path(path).parent
        if not scene:
            raise RuntimeError("model {} failed to load!".format(path))
        self.directory = os.path.abspath(os.path.dirname(path))
        for mesh in scene.meshes:
            number_vertices = len(mesh.vertices)
            number_normals = len(mesh.normals)
            number_texturecoords = len(mesh.texturecoords)
            number_tangents = len(mesh.tangents)
            number_bitangents = len(mesh.bitangents)
            if number_normals > 0:
                normals = mesh.normals
            else:
                normals = np.zeros(
                    shape=(number_vertices, 3), dtype=np.float32)
            texcoords = np.zeros(shape=(number_vertices, 2), dtype=np.float32)
            if number_texturecoords > 0:
                # texcoords need to compute 1 - y to follow OpenGL convention
                for i in range(number_vertices):
                    texcoords[i][0] = mesh.texturecoords[0, i, 0]
                    texcoords[i][1] = mesh.texturecoords[0, i, 1]
                if number_tangents > 0:
                    tangents = mesh.tangents
                else:
                    tangents = np.zeros(
                        shape=(number_vertices, 3), dtype=np.float32)
                if number_bitangents > 0:
                    bitangents = mesh.bitangents
                else:
                    bitangents = np.zeros(
                        shape=(number_vertices, 3), dtype=np.float32)
            number_faces = len(mesh.faces)
            indices = np.zeros(shape=(number_faces * 3), dtype=np.int32)
            for i in range(number_faces):
                face = mesh.faces[i]
                # retrieve all indices of the face and store them in the indices vector
                for j in range(3):
                    indices[i*3+j] = face[j]
            # process materials
            textures = []
            material = scene.materials[mesh.materialindex]
            # 1. diffuse maps
            diffuseMaps = self.loadMaterialTextures(
                material, pyassimp.material.aiTextureType_DIFFUSE, "texture_diffuse")
            textures.extend(diffuseMaps)
            # 2. specular maps
            specularMaps = self.loadMaterialTextures(
                material, pyassimp.material.aiTextureType_SPECULAR, "texture_specular")
            textures.extend(specularMaps)
            # 3. normal maps
            normalMaps = self.loadMaterialTextures(
                material, pyassimp.material.aiTextureType_HEIGHT, "texture_normal")
            textures.extend(normalMaps)
            # 4. height maps
            heightMaps = self.loadMaterialTextures(
                material, pyassimp.material.aiTextureType_AMBIENT, "texture_height")
            textures.extend(heightMaps)

            newmesh = Mesh(mesh.vertices, normals, texcoords,
                           tangents, bitangents, indices, textures)
            self.meshes.append(newmesh)

    def loadMaterialTextures(self, mat:pyassimp.structs.Material, type:int, typeName:str) -> list[MeshTexture]:
        textures: list[MeshTexture] = []
        texture_files = mat.properties.get(('file', type))
        if texture_files:
            # check if texture was loaded before and if so, continue to next iteration: skip loading a new texture
            skip = False
            for texture in self.textures_loaded:
                if texture.path == texture_files:
                    textures.append(texture)
                    skip = True
                    break
            if not skip:
                texture = MeshTexture()
                texture.tex = ImageTexture2D(os.path.join(
                    self.directory, texture_files))
                texture.type = typeName
                texture.path = texture_files
                textures.append(texture)
                # store it as texture loaded for entire model, to ensure we won't unnecessary load duplicate textures.
                self.textures_loaded.append(texture)
        return textures
