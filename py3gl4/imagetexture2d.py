from OpenGL.GL import *
import imageio.v3 as iio
from PIL import Image
import numpy as np

class ImageTexture2D:
    def __init__(self, file_path: str, flip_y: bool = False, 
                 srgb: bool = False) -> None:
        tex = np.empty(1, np.uint32)
        glCreateTextures(GL_TEXTURE_2D, 1, tex)
        self.tex_id = tex[0]
        if flip_y:
            image = Image.open(file_path).transpose(Image.FLIP_TOP_BOTTOM)
        else:
            image = Image.open(file_path)
        self.width, self.height = image.size
        channels = len(image.getbands())
        if channels == 1:
            self.pixel_format = GL_RED
            self.internal_format = GL_R32F
        elif channels == 2:
            self.pixel_format = GL_RG
            self.internal_format = GL_RG32F
        elif channels == 3:
            self.pixel_format = GL_RGB
            if srgb:
                self.internal_format = GL_SRGB
            else:
                self.internal_format = GL_RGB32F
        elif channels == 4:
            self.pixel_format = GL_RGBA
            if srgb:
                self.internal_format = GL_SRGB_ALPHA
            else:
                self.internal_format = GL_RGBA32F
        glTextureStorage2D(self.tex_id, 1, self.internal_format, self.width, self.height) 
        glTextureSubImage2D(self.tex_id, 0, 0, 0, self.width, self.height,
                            self.pixel_format, GL_UNSIGNED_BYTE, image.tobytes())
        glGenerateTextureMipmap(self.tex_id)

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

class HDRImageTexture2D:
    def __init__(self, file_path: str, flip_ud: bool = False) -> None:
        tex = np.empty(1, np.uint32)
        glCreateTextures(GL_TEXTURE_2D, 1, tex)
        self.tex_id = tex[0]
        img = iio.imread(file_path) #.transpose((1))
        height, width, channels = img.shape
        if flip_ud:
            img = np.flipud(img)
        if channels == 1:
            self.pixel_format = GL_RED
            self.internal_format = GL_R32F
        elif channels == 2:
            self.pixel_format = GL_RG
            self.internal_format = GL_RG32F
        elif channels == 3:
            self.pixel_format = GL_RGB
            self.internal_format = GL_RGB32F
        elif channels == 4:
            self.pixel_format = GL_RGBA
            self.internal_format = GL_RGBA32F
        dtype = img.dtype
        if dtype == np.uint8:
            self.pixel_type = GL_UNSIGNED_BYTE
        elif dtype == np.float32:
            self.pixel_type = GL_FLOAT
        else:
            self.pixel_type = GL_UNSIGNED_BYTE
        self.width = width
        self.height = height
        glTextureStorage2D(self.tex_id, 1, self.internal_format, width, height) 
        glTextureSubImage2D(self.tex_id, 0, 0, 0, width, height,
                            self.pixel_format, self.pixel_type, img.tobytes())

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

