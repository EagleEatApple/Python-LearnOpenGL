from OpenGL.GL import *
from numpy import empty, uint32


class TextureCubemap:
    def __init__(self, internal_format: int, width: int, height: int, level:int=1) -> None:
        tex = empty(1, uint32)
        glCreateTextures(GL_TEXTURE_CUBE_MAP, 1, tex)
        self.tex_id = tex[0]
        self.internal_format = internal_format
        self.width = width
        self.height = height
        glTextureStorage2D(self.tex_id, level, internal_format, width, height)

    def bind(self, index: int) -> None:
        glBindTextureUnit(index, self.tex_id)

    def delete(self) -> None:
        if glIsTexture(self.tex_id):
            glDeleteTextures(1, self.tex_id)

    def setFiltering(self, min_filter: int, mag_filter: int) -> None:
        glTextureParameteri(self.tex_id, GL_TEXTURE_MIN_FILTER, min_filter)
        glTextureParameteri(self.tex_id, GL_TEXTURE_MAG_FILTER, mag_filter)

    def setWrapMode(self, wrap_s: int, wrap_t: int, wrap_r:int) -> None:
        glTextureParameteri(self.tex_id, GL_TEXTURE_WRAP_S, wrap_s)
        glTextureParameteri(self.tex_id, GL_TEXTURE_WRAP_T, wrap_t)
        glTextureParameteri(self.tex_id, GL_TEXTURE_WRAP_R, wrap_r)

    def generateMipmap(self)->None:
        glGenerateTextureMipmap(self.tex_id)