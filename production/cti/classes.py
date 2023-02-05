from enum import Enum, auto
from typing import List, Optional, Any, Tuple

from compiler.lexer.static import *

DEFAULT_MOVE = 1.0
DEFAULT_ROTATION = 15.0
DEFAULT_BRUSH_CHANGE = 1.0
STARTING_ROTATION = 0.0


class CTI(Enum):
    MOVE = auto()
    ROTATE = auto()
    BRUSH = auto()
    STACK = auto()
    PEN = auto()


class STACK_EVENT(Enum):
    PUSH = auto()
    POP = auto()


class PEN_EVENT(Enum):
    UP = auto()
    DOWN = auto()


class ROTATE_EVENT(Enum):
    YAW = auto()
    ROLL = auto()
    PITCH = auto()


class BRUSH_EVENT(Enum):
    INCREASE = auto()
    DECREASE = auto()


class Instruction:
    type: CTI

    def __eq__(self, other):
        return self.type == other.type

    def can_combine(self, other) -> bool:
        raise NotImplementedError

    # Always check can combine before
    def combine(self, other) -> List:
        raise NotImplementedError

    def __str__(self):
        return f"{self.__class__.__name__}" \
               f"({', '.join([str(v) for k, v  in self.__dict__.items() if not k.startswith('__')])})"

    def __repr__(self):
        return str(self)


class MOVE(Instruction):
    type = CTI.MOVE
    move_amount: float

    def __init__(self, move_amount: float = DEFAULT_MOVE):
        self.move_amount = move_amount

    def can_combine(self, other):
        return self == other

    def combine(self, other):
        self.move_amount += other.move_amount
        return [self]


class ROTATE(Instruction):
    type = CTI.ROTATE
    rotate_yaw: float = STARTING_ROTATION
    rotate_roll: float = STARTING_ROTATION
    rotate_pitch: float = STARTING_ROTATION

    def __init__(self, rotate_event: ROTATE_EVENT, rotate_amount: float = DEFAULT_ROTATION):
        if rotate_event == ROTATE_EVENT.YAW:
            self.rotate_yaw = rotate_amount
        elif rotate_event == ROTATE_EVENT.ROLL:
            self.rotate_roll = rotate_amount
        elif rotate_event == ROTATE_EVENT.PITCH:
            self.rotate_pitch = rotate_amount

    def can_combine(self, other):
        return self == other

    def combine(self, other):
        self.rotate_yaw += other.rotate_yaw
        self.rotate_roll += other.rotate_roll
        self.rotate_pitch += other.rotate_pitch
        return [self]


class BRUSH(Instruction):
    type = CTI.BRUSH
    brush_change: float

    def __init__(self, brush_event: BRUSH_EVENT, brush_change: float = DEFAULT_BRUSH_CHANGE):
        # If increase use addition, if decrease use subtraction
        if brush_event == BRUSH_EVENT.INCREASE:
            self.brush_change += brush_change
        elif brush_event == BRUSH_EVENT.DECREASE:
            self.brush_change -= brush_change

    def can_combine(self, other):
        return self == other

    def combine(self, other):
        self.brush_change += other.brush_change
        return [self]


class STACK(Instruction):
    type = CTI.STACK
    stack_event: STACK_EVENT

    def __init__(self, stack_event: STACK_EVENT):
        self.stack_event = stack_event

    def can_combine(self, other):
        if self != other:
            return False

        # If '[]' occurs it can be removed
        if self.stack_event == STACK_EVENT.POP and other.stack_event == STACK_EVENT.PUSH:
            return False

        return True

    def combine(self, other):
        return []


class PEN(Instruction):
    type = CTI.PEN
    pen_event: PEN_EVENT

    def __init__(self, pen_event: PEN_EVENT):
        self.pen_event = pen_event

    def can_combine(self, other):
        if self != other:
            return False

        if self.pen_event == PEN_EVENT.UP and other.pen_event == PEN_EVENT.DOWN:
            return True
        elif self.pen_event == PEN_EVENT.DOWN and other.pen_event == PEN_EVENT.UP:
            return True
        return False

    def combine(self, other):
        return []


def ltoken_to_instruction(ltoken: str, values: Optional[Tuple[Any]]) -> Instruction:
    # Value based tokens
    if ltoken in BASE_AXIOMS:
        assert (len(values) == 1 and isinstance(values[0], float)) or len(values) == 0
        return MOVE(*values)

    elif ltoken in ROTATION_TOKENS:
        assert (len(values) == 1 and isinstance(values[0], float)) or len(values) == 0

        if ltoken in YAW:
            return ROTATE(ROTATE_EVENT.YAW, *values)
        elif ltoken in PITCH:
            return ROTATE(ROTATE_EVENT.PITCH, *values)
        elif ltoken in ROLL:
            return ROTATE(ROTATE_EVENT.ROLL, *values)

    elif ltoken in BRUSH_TOKENS:
        assert (len(values) == 1 and isinstance(values[0], float)) or len(values) == 0

        if ltoken in BRUSH_INCREASE_SIZE:
            return BRUSH(BRUSH_EVENT.INCREASE, *values[0])
        elif ltoken in BRUSH_DECREASE_SIZE:
            return BRUSH(BRUSH_EVENT.DECREASE, *values[0])

    # Enum Based Tokens
    elif ltoken in STACK_TOKENS:
        assert len(values) == 0

        if ltoken in STACK_PUSH:
            return STACK(STACK_EVENT.PUSH)
        elif ltoken in STACK_POP:
            return STACK(STACK_EVENT.POP)

    elif ltoken in PEN_TOKENS:
        assert len(values) == 0

        if ltoken in PEN_UP:
            return PEN(PEN_EVENT.UP)
        elif ltoken in PEN_DOWN:
            return PEN(PEN_EVENT.DOWN)

    raise NotImplementedError("")
