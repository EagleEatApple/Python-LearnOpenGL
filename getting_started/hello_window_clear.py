import sys
parent_dir = "../Python-LearnOpenGL"
sys.path.append(parent_dir)

from OpenGL.GL import *

from py3gl4 import *
from app import *

class HelloWindowClear(GLWindow):
    def init(self) -> None:
        pass

    def cleanup(self) -> None:
        pass

    def render(self) -> None:
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

if __name__ == "__main__":
    app = App()
    win = HelloWindowClear(title="Hello, Window!")
    app.run(win)