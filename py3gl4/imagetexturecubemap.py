from OpenGL.GL import *
from numpy import ndarray, empty, uint32

from PIL import Image

# the order of list : right, left, top, bottom, front, back
class ImageTextureCubemap:
    def __init__(self, filenames:list[str], mipmap_levels:int=1, srgb:bool=False) -> None:
        tex = empty(1, uint32)
        glCreateTextures(GL_TEXTURE_CUBE_MAP, 1, tex)
        self.tex_id = tex[0]
        image = Image.open(filenames[0])
        if image is not None:
            self.width, self.height = image.size
            channels = len(image.getbands())
            if channels == 1:
                self.pixel_format = GL_RED
                self.internal_format = GL_R32F
            elif channels == 2:
                self.pixelFormat = GL_RG
                self.internalFormat = GL_RG32F
            elif channels == 3:
                self.pixel_format = GL_RGB
                if srgb:
                    self.internal_format = GL_SRGB8
                else:
                    self.internal_format = GL_RGB32F
            elif channels == 4:
                self.pixel_format = GL_RGBA
                if srgb:
                    self.internal_format = GL_SRGB8_ALPHA8
                else:
                    self.internal_format = GL_RGBA32F
            glTextureStorage2D(self.tex_id, mipmap_levels, self.internal_format, self.width, self.height)
            for i in range(6):
                image = Image.open(filenames[i])
                glTextureSubImage3D(self.tex_id, 0, 0, 0, i, self.width, self.height, 1, self.pixel_format, GL_UNSIGNED_BYTE, image.tobytes())

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