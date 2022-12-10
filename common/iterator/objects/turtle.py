from __future__ import annotations
from typing import Optional


class Turtle:
    # Access Turtle for global stand
    # Access the Turtle() instance for local point
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    yaw: float = 0.0
    roll: float = 0.0
    pitch: float = 0.0

    def __init__(self):
        # Returns an instance copy that is only valid for the state.
        [self.__setattr__(attr, Turtle.__getattribute__(Turtle, attr))
         for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]

    def position(self: Optional[Turtle] = None) -> (float, float, float):
        # Returns the position of the turtle or the turtle instance
        if self is None:
            return Turtle.x, Turtle.y, Turtle.z
        else:
            return self.x, self.y, self.z

    def heading(self: Optional[Turtle] = None) -> (float, float, float):
        # Returns the heading of the turtle or the turtle instance
        if self is None:
            return Turtle.yaw, Turtle.roll, Turtle.pitch
        else:
            return self.yaw, self.roll, self.pitch

    @classmethod
    def load(cls, self: Turtle):
        # Set global turtle to turtle objects location
        [cls.__class__.__setattr__(cls, attr, self.__getattribute__(attr))
         for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]


if __name__ == '__main__':
    Turtle.x += 1
    t = Turtle()
    print(t.position(), Turtle.position())
    Turtle.x += 1
    Turtle.y += 1
    Turtle.z += 1
    print(t.position(), Turtle.position())
    Turtle.load(t)
    print(t.position(), Turtle.position())
