from compiler.Lglobal.objects.turtle import Turtle


# This class acts as an interface
class TL:
    @classmethod
    def x(cls) -> float: return Turtle.x

    @classmethod
    def y(cls) -> float: return Turtle.y

    @classmethod
    def z(cls) -> float: return Turtle.z

    @classmethod
    def yaw(cls) -> float: return Turtle.yaw

    @classmethod
    def roll(cls) -> float: return Turtle.roll

    @classmethod
    def pitch(cls) -> float: return Turtle.pitch
