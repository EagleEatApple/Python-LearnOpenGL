from OpenGL.GL import *
from numpy import ndarray, empty, uint32
import glm

class Texture2D:
    def __init__(self, level: int, internal_format: int, width: int, height: int, pixel_format:int, pixel_type:int,data:ctypes.c_void_p = None) -> None:
        tex = empty(1, uint32)
        glCreateTextures(GL_TEXTURE_2D, 1, tex)
        self.tex_id = tex[0]
        self.level = level
        self.internal_format = internal_format
        self.width = width
        self.height = height
        self.pixel_format = pixel_format
        self.pixel_type = pixel_type
        glTextureStorage2D(self.tex_id, level,internal_format, width, height)
        glTextureSubImage2D(self.tex_id, 0, 0, 0, width, height,
                            pixel_format, pixel_type, data)


    def bind(self, index: int) -> None:
        glBindTextureUnit(index, self.tex_id)

    def delete(self) -> None:
        if glIsTexture(self.tex_id):
            glDeleteTextures(1, self.tex_id)

    def setFiltering(self, min_filter: int, mag_filter: int) -> None:
        glTextureParameteri(self.tex_id, GL_TEXTURE_MIN_FILTER, min_filter)
        glTextureParameteri(self.tex_id, GL_TEXTURE_MAG_FILTER, mag_filter)

    def setWrapMode(self, wrap_s: int, wrap_t: int) -> None:
        glTextureParameteri(self.tex_id, GL_TEXTURE_WRAP_S, wrap_s)
        glTextureParameteri(self.tex_id, GL_TEXTURE_WRAP_T, wrap_t)

    def setBorderColor(self, color:glm.vec4)-> None:
        glTextureParameterfv(self.tex_id, GL_TEXTURE_BORDER_COLOR, glm.value_ptr(color))

