from OpenGL.GL import *
from numpy import ndarray, empty, uint32

from py3gl4.texture2d import Texture2D
from py3gl4.renderbuffer import Renderbuffer, RenderbufferMultisample
from py3gl4.texture2dmultisample import Texture2DMultisample
from py3gl4.texturecubemap import TextureCubemap

class Framebuffer:
    def __init__(self) -> None:
        self.width = 0
        self.height = 0
        fbo = empty(1, uint32)
        glCreateFramebuffers(1, fbo)
        self.fbo_id = fbo[0]

    def bind(self) -> None:
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo_id)

    def read(self)->None:
        glBindFramebuffer(GL_READ_FRAMEBUFFER, self.fbo_id)

    def draw(self)->None:
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, self.fbo_id)

    def delete(self) -> None:
        if glIsFramebuffer(self.fbo_id):
            glDeleteFramebuffers(1, self.fbo_id)

    def attachTexture2D(self, attachment: int, texture: Texture2D,	level: int) -> None:
        glNamedFramebufferTexture(
            self.fbo_id, attachment, texture.tex_id, level)
        self.width = texture.width
        self.height = texture.height

    def attachTexture2DMultisample(self, attachment: int, texture: Texture2DMultisample,	level: int) -> None:
        glNamedFramebufferTexture(
            self.fbo_id, attachment, texture.tex_id, level)
        self.width = texture.width
        self.height = texture.height

    def attachTextureCubemap(self, attachment: int, texture: TextureCubemap, level: int) -> None:
        glNamedFramebufferTexture(
            self.fbo_id, attachment, texture.tex_id, level)
        self.width = texture.width
        self.height = texture.height

    def attachRenderbuffer(self, attachment: int, renderbuffertarget:int, renderbuffer: Renderbuffer) -> None:
        glNamedFramebufferRenderbuffer(self.fbo_id, attachment, renderbuffertarget, renderbuffer.rbo_id)

    def attachRenderbufferMultisample(self, attachment: int, renderbuffertarget:int, renderbuffer: RenderbufferMultisample) -> None:
        glNamedFramebufferRenderbuffer(self.fbo_id, attachment, renderbuffertarget, renderbuffer.rbo_id)

    def isComplete(self) -> bool:
        return (glCheckNamedFramebufferStatus(self.fbo_id, GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE)

    def Blit(self, target:"Framebuffer", mask, filter) -> None:
        glBlitNamedFramebuffer(self.fbo_id, target.fbo_id,
            0,0,self.width,self.height,0,0,target.width,target.height, 
            mask, filter)

    def setDrawBuffer(self, buf:int)-> None:
        glNamedFramebufferDrawBuffer(self.fbo_id, buf)

    def setDrawBuffers(self, buf:list[int])-> None:
        glNamedFramebufferDrawBuffers(self.fbo_id, len(buf), buf)

    def setReadBuffer(self, buf:int)-> None:
        glNamedFramebufferReadBuffer(self.fbo_id, buf)

    def setTextureLayer(self, attachment:int, texture:int, level:int, layer:int):
        glNamedFramebufferTextureLayer(self.fbo_id, attachment, texture, level, layer) 