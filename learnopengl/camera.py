from enum import Enum
from math import sin, cos, radians

from glm import vec3, mat4x4, radians, normalize, cross, lookAt


# Defines several possible options for camera movement. Used as abstraction to stay away from window-system specific input methods
class Camera_Movement(Enum):
    FORWARD = 0
    BACKWARD = 1
    LEFT = 2
    RIGHT = 3


# Default camera values
YAW = -90.0
PITCH = 0.0
SPEED = 2.5
SENSITIVITY = 0.1
ZOOM = 45.0


#  An abstract camera class that processes input and calculates the corresponding Euler Angles, Vectors and Matrices for use in OpenGL
class Camera:
    def __init__(self, position=vec3(0.0, 0.0, 0.0), up=vec3(0.0, 1.0, 0.0), yaw=YAW, pitch=PITCH,
                 front=vec3(0.0, 0.0, -1.0), speed=SPEED, sensitivity=SENSITIVITY, zoom=ZOOM) -> None:
        # camera Attributes
        self.position = position
        self.front = front
        self.up = None
        self.right = None
        self.worldUp = up
        # euler Angles
        self.yaw = yaw
        self.pitch = pitch
        # camera options
        self.movementSpeed = speed
        self.mouseSensitivity = sensitivity
        self.zoom = zoom
        self.updateCameraVectors()

    # returns the view matrix calculated using Euler Angles and the LookAt Matrix
    def GetViewMatrix(self) -> mat4x4:
        return lookAt(self.position, self.position + self.front, self.up)

    # processes input received from any keyboard-like input system. Accepts input parameter in the form of camera defined ENUM (to abstract it from windowing systems)
    def ProcessKeyboard(self, direction: Camera_Movement, deltaTime: float) -> None:
        velocity = self.movementSpeed * deltaTime
        if direction == Camera_Movement.FORWARD:
            self.position += self.front * velocity
        if direction == Camera_Movement.BACKWARD:
            self.position -= self.front * velocity
        if direction == Camera_Movement.LEFT:
            self.position -= self.right * velocity
        if direction == Camera_Movement.RIGHT:
            self.position += self.right * velocity

    # processes input received from a mouse input system. Expects the offset value in both the x and y direction
    def ProcessMouseMovement(self, xoffset: float, yoffset: float, constrainPitch=True) -> None:
        xoffset *= self.mouseSensitivity
        yoffset *= self.mouseSensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        # make sure that when pitch is out of bounds, screen doesn't get flipped
        if constrainPitch:
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0

        # update Front, Right and Up Vectors using the updated Euler angles
        self.updateCameraVectors()

    # processes input received from a mouse scroll-wheel event. Only requires input on the vertical wheel-axis
    def ProcessMouseScroll(self, yoffset: float) -> None:
        self.zoom -= yoffset
        if self.zoom < 1.0:
            self.zoom = 1.0
        if self.zoom > 45.0:
            self.zoom = 45.0

    # calculates the front vector from the Camera's (updated) Euler Angles
    def updateCameraVectors(self) -> None:
        front = vec3()
        front.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.yaw)) * cos(radians(self.pitch))
        self.front = normalize(front)
        # also re-calculate the Right and Up vector
        self.right = normalize(cross(self.front, self.worldUp))
        self.up = normalize(cross(self.right, self.front))
