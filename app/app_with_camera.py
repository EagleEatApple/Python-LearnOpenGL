import sys
parent_dir = "../Python-LearnOpenGL"
sys.path.append(parent_dir)
import glfw
from OpenGL.GL import *
import glm

from learnopengl import Camera, Camera_Movement

class CameraWindow():
    def __init__(self, width: int = 800, height: int = 600,
                 title: str = 'Hello, OpenGL 4.6!') -> None:
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 6)
        glfw.window_hint(glfw.SAMPLES, 4)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)


        self.id = glfw.create_window(width, height, title, None, None)
        if (self.id == None):
            print("Failed to create GLFW window")
        else:
            glfw.make_context_current(self.id)
            glfw.set_window_size_callback(self.id, self.resize)
            #glfw.set_key_callback(self.id, self.key_input)
            glfw.set_scroll_callback(self.id, self.mouse_wheel)
            glfw.set_cursor_pos_callback(self.id, self.mouse_move)
            glfw.set_input_mode(self.id, glfw.CURSOR, glfw.CURSOR_DISABLED)
        self.camera = Camera(glm.vec3(0, 0, 3.0))
        self.firstMouse = True
        self.width, self.height = glfw.get_window_size(self.id)
        self.lastX = float(self.width)/2
        self.lastY = float(self.height)/2
        self.deltaTime = 0.0
        self.lastFrame = 0.0

    def init(self) -> None:
        #raise NotImplementedError
        pass

    def render(self) -> None:
        currentFrame = glfw.get_time()
        self.deltaTime = currentFrame - self.lastFrame
        self.lastFrame = currentFrame
        #glfw.set_key_callback(self.id, self.key_input)
        self.key_input()

    def cleanup(self) -> None:
        #raise NotImplementedError
        pass

    def resize(self, window, width, height)-> None:
        glViewport(0, 0, width, height)


    def key_input(self)-> None:
        if glfw.get_key(self.id, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(self.id, True)
        if glfw.get_key(self.id, glfw.KEY_W) == glfw.PRESS:
            self.camera.ProcessKeyboard(Camera_Movement.FORWARD, self.deltaTime)
        if glfw.get_key(self.id, glfw.KEY_S) == glfw.PRESS:
            self.camera.ProcessKeyboard(Camera_Movement.BACKWARD, self.deltaTime)
        if glfw.get_key(self.id, glfw.KEY_A) == glfw.PRESS:
            self.camera.ProcessKeyboard(Camera_Movement.LEFT, self.deltaTime)
        if glfw.get_key(self.id, glfw.KEY_D) == glfw.PRESS:
            self.camera.ProcessKeyboard(Camera_Movement.RIGHT, self.deltaTime)


    def mouse_move(self, window, xpos, ypos)->None:
        if self.firstMouse:
            self.lastX = xpos
            self.lastY = ypos
            self.firstMouse = False

        xoffset = xpos - self.lastX
        yoffset = self.lastY - ypos

        self.lastX = xpos
        self.lastY = ypos

        self.camera.ProcessMouseMovement(xoffset, yoffset)

    def mouse_wheel(self, window, xoffset, yoffset)-> None:
        self.camera.ProcessMouseScroll(yoffset)



class App():
    def __init__(self) -> None:
        glfw.init()

    def run(self, window) -> None:
        window.init()
        while not glfw.window_should_close(window.id):
            window.render()
            glfw.swap_buffers(window.id)
            glfw.poll_events()
        window.cleanup()
        glfw.destroy_window(window.id)
        glfw.terminate()


if __name__ == "__main__":
    app = App()
    win = CameraWindow(400,300)
    app.run(win)
