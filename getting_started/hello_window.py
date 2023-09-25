import sys
parent_dir = "../Python-LearnOpenGL"
sys.path.append(parent_dir)

from app import *

class HelloWindow(GLWindow):
    def init(self) -> None:
        pass

    def cleanup(self) -> None:
        pass

    def render(self) -> None:
        pass

if __name__ == "__main__":
    app = App()
    win = HelloWindow(title="Hello, Window!")
    app.run(win)