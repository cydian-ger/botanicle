# from __future__ import annotations ruins annotations
from typing import Optional


class Turtle:
    """
    THIS IS A TEST DOC STRING
    """
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

    # self: Optional[Turtle]
    def position(self=None) -> (float, float, float):
        # Returns the position of the turtle or the turtle instance
        if self is None:
            return Turtle.x, Turtle.y, Turtle.z
        else:
            return self.x, self.y, self.z

    # self Optional[Turtle]
    def heading(self=None) -> (float, float, float):
        # Returns the heading of the turtle or the turtle instance
        if self is None:
            return Turtle.yaw, Turtle.roll, Turtle.pitch
        else:
            return self.yaw, self.roll, self.pitch

    @classmethod
    def load(cls, self):
        # Set global turtle to turtle objects location
        [cls.__class__.__setattr__(cls, attr, self.__getattribute__(attr))
         for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
