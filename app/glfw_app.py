import glfw
from OpenGL.GL import *

class GLWindow():
    def __init__(self, width: int = 800, height: int = 600,
                 title: str = 'Hello, OpenGL 4.6!') -> None:
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 6)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        self.id = glfw.create_window(width, height, title, None, None)
        if (self.id == None):
            print("Failed to create GLFW window")
        else:
            glfw.make_context_current(self.id)
            glfw.set_window_size_callback(self.id, self.resize)
            glfw.set_scroll_callback(self.id, self.mouse_wheel)
            glfw.set_cursor_pos_callback(self.id, self.mouse_move)
            glfw.set_input_mode(self.id, glfw.CURSOR, glfw.CURSOR_DISABLED)
            # self.active = True

    def init(self) -> None:
        #raise NotImplementedError
        pass

    def render(self) -> None:
        pass

    def cleanup(self) -> None:
        #raise NotImplementedError
        pass

    def resize(self, window, width, height)-> None:
        glViewport(0, 0, width, height)

    def key_input(self)-> None:
        if glfw.get_key(self.id, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(self.id, True)
    
    def mouse_wheel(self, window, xoffset, yoffset)-> None:
        pass

    def mouse_move(self, window, xposIn, yposIn)->None:
        pass



class App():
    def __init__(self) -> None:
        glfw.init()

    def run(self, window:GLWindow) -> None:
        window.init()
        while not glfw.window_should_close(window.id):
            window.key_input()
            window.render()
            glfw.swap_buffers(window.id)
            glfw.poll_events()
        window.cleanup()
        glfw.destroy_window(window.id)
        glfw.terminate()


if __name__ == "__main__":
    app = App()
    win = GLWindow(400,300)
    app.run(win)
