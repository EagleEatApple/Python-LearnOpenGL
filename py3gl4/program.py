import numpy as np
from OpenGL.GL import *

from py3gl4.shader import Shader
import glm

class Program:
    def __init__(self, shaders: list[Shader]) -> None:
        self.program_id = glCreateProgram()
        for shader in shaders:
            glAttachShader(self.program_id, shader.shader_id)
        glLinkProgram(self.program_id)

    def use(self) -> None:
        glUseProgram(self.program_id)

    def delete(self) -> None:
        if glIsProgram(self.program_id):
            glDeleteProgram(self.program_id)

    def setUniform4f(self, name:str, v0: float, v1: float, v2: float, v3: float) -> None:
        location = glGetUniformLocation(self.program_id, name)
        glUniform4f(location, v0, v1, v2, v3)

    def setUniform1i(self, name:str, value: int) -> None:
        location = glGetUniformLocation(self.program_id, name)
        glUniform1i(location, value)

    def setUniformMatrix4fv(self, name:str, mat: glm.mat4x4) -> None:
        location = glGetUniformLocation(self.program_id, name)
        glUniformMatrix4fv(location, 1, False, glm.value_ptr(mat))

    def setUniform3f(self, name:str, v0: float, v1: float, v2: float) -> None:
        location = glGetUniformLocation(self.program_id, name)
        glUniform3f(location, v0, v1, v2)

    def setUniform2fv(self, name:str, value:glm.vec2) -> None:
        location = glGetUniformLocation(self.program_id, name)
        glUniform2fv(location, 1, glm.value_ptr(value))
    
    def setUniform3fv(self, name:str, value:glm.vec3) -> None:
        location = glGetUniformLocation(self.program_id, name)
        glUniform3fv(location, 1, glm.value_ptr(value))

    def setUniform4fv(self, name:str, value:glm.vec4) -> None:
        location = glGetUniformLocation(self.program_id, name)
        glUniform4fv(location, 1, glm.value_ptr(value))

    def setUniform1f(self, name:str, value: float) -> None:
        location = glGetUniformLocation(self.program_id, name)
        glUniform1f(location, value)

    def setUBOBinding(self, name:str, binding_point:int)->None:
        index = glGetUniformBlockIndex(self.program_id, name)
        glUniformBlockBinding(self.program_id, index, binding_point)



class ProgramVF(Program):
    def __init__(self, vertex_source_path:str, fragment_source_path:str) -> None:
        vertex_shader = Shader(GL_VERTEX_SHADER, vertex_source_path)
        fragment_shader = Shader(GL_FRAGMENT_SHADER, fragment_source_path)
        super().__init__([vertex_shader, fragment_shader])
        vertex_shader.delete()
        fragment_shader.delete()

class ProgramVGF(Program):
    def __init__(self, vertex_source_path:str, geometry_source_path:str, fragment_source_path:str) -> None:
        vertex_shader = Shader(GL_VERTEX_SHADER, vertex_source_path)
        geometry_shader = Shader(GL_GEOMETRY_SHADER, geometry_source_path)
        fragment_shader = Shader(GL_FRAGMENT_SHADER, fragment_source_path)
        super().__init__([vertex_shader, geometry_shader, fragment_shader])
        vertex_shader.delete()
        geometry_shader.delete()
        fragment_shader.delete()