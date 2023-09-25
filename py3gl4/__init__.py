import ctypes
from py3gl4.shader import Shader
from py3gl4.program import ProgramVF,ProgramVGF,Program
from py3gl4.vertexarrayobject import VertexAttribute, VertexArrayObject
from py3gl4.vertexbufferobject import VertexBufferObject
from py3gl4.elementbufferobject import ElementBufferObject
from py3gl4.imagetexture2d import ImageTexture2D, HDRImageTexture2D
from py3gl4.texture2d import Texture2D
from py3gl4.renderbuffer import Renderbuffer, RenderbufferMultisample
from py3gl4.framebuffer import Framebuffer
from py3gl4.imagetexturecubemap import ImageTextureCubemap
from py3gl4.uniformbufferobject import UniformBufferObject
from py3gl4.texture2dmultisample import Texture2DMultisample
from py3gl4.texturecubemap import TextureCubemap


GLFLOAT = ctypes.c_float
GLUINT = ctypes.c_uint
CLINT = ctypes.c_int
