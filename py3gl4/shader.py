from OpenGL.GL import *

class Shader:
    def __init__(self, type: int, file_name:str) -> None:
        self.shader_id = glCreateShader(type)
        with open(file_name) as file:
            source = file.read()
            glShaderSource(self.shader_id, source)
            glCompileShader(self.shader_id)

    def delete(self)-> None:
        if glIsShader(self.shader_id):
            glDeleteShader(self.shader_id)

