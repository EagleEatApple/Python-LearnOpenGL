from OpenGL.GL import *
from numpy import ndarray, empty, uint32
import glm

class Texture2DMultisample:
    def __init__(self, samples: int, internal_format: int, width: int, height: int, fixed_sample_locations:bool=True) -> None:
        tex = empty(1, uint32)
        glCreateTextures(GL_TEXTURE_2D_MULTISAMPLE, 1, tex)
        self.tex_id = tex[0]
        self.samples = samples
        self.internal_format = internal_format
        self.width = width
        self.height = height
        self.fixed_sample_locations = fixed_sample_locations
        glTextureStorage2DMultisample(self.tex_id, samples, internal_format, width, height, fixed_sample_locations)

    def delete(self) -> None:
        if glIsTexture(self.tex_id):
            glDeleteTextures(1, self.tex_id)
