from typing import List, Tuple, Any

from compiler.lexer.static import *
from production.cti.classes import CTI, STACK_EVENT, PEN_EVENT, DEFAULT_MOVE, DEFAULT_ROTATION


def add_move_token(out_tokens: List[Tuple[CTI, Any]], ltoken: Tuple[str, Any]):
    # Default the value to 1
    value = ltoken[1] if len(ltoken) > 1 else DEFAULT_MOVE

    if out_tokens[-1][0] == CTI.MOVE:
        out_tokens[-1] = (CTI.MOVE, out_tokens[-1][1] + value)
    else:
        out_tokens.append((CTI.MOVE, value))
    return


def add_rotation_token(out_tokens: List[Tuple[CTI, Any]], ltoken: Tuple[str, float]):
    # (yaw, roll, pitch)
    values = (0, 0, 0)

    rotation_value = ltoken[1] if len(ltoken) > 1 else DEFAULT_ROTATION

    if ltoken[0] in TILT:
        values = (rotation_value, 0.0, 0.0)
    elif ltoken[0] in TURN:
        values = (0.0, 0.0, rotation_value)
    elif ltoken[0] in TWIST:
        values = (0.0, rotation_value, 0.0)

    if out_tokens[-1][0] == CTI.ROTATE:
        out_tokens[-1] = (CTI.ROTATE,
                          out_tokens[-1][1] + values[0],
                          out_tokens[-1][2] + values[1],
                          out_tokens[-1][3] + values[2]
                          )
    else:
        out_tokens.append((CTI.MOVE, *values))


def add_stack_token(out_tokens: List[Tuple[CTI, Any]], ltoken: Tuple[str, Any]):
    # If Stack Push is immediately followed by Stack Pop it does not have an effect
    # And thus should be culled
    if out_tokens[-1] == (CTI.STACK, STACK_EVENT.PUSH) and ltoken[0] == STACK_POP:
        out_tokens.pop(-1)
        return

    if ltoken[0] == STACK_POP:
        out_tokens.append((CTI.STACK, STACK_EVENT.POP))
    elif ltoken[0] == STACK_PUSH:
        out_tokens.append((CTI.STACK, STACK_EVENT.PUSH))
    return


def add_pen_token(out_tokens: List[Tuple[CTI, Any]], ltoken: Tuple[str, Any]):
    if ltoken[0] == PEN_DOWN:
        new_ltoken = PEN_EVENT.DOWN
    elif ltoken[0] == PEN_UP:
        new_ltoken = PEN_EVENT.UP
    else:
        raise NotImplementedError()

    # If the previous token is the opposite, remove it from the
    if out_tokens[-1][0] == CTI.PEN and out_tokens[-1][1] != new_ltoken:
        out_tokens.pop(-1)
        return

    out_tokens.append((CTI.PEN, new_ltoken))


def result_to_cti(result_list: List[Tuple[str, Any]]):
    # List of tokens that are returned to cti
    # TODO
    # Make a CTI class
    # With add and shit
    raise NotImplementedError("FINISH MAKING THE CLASSES")

    out_tokens = list([("",)])

    for ltoken in result_list:
        name = ltoken[0]

        # Value based tokens
        if name in BASE_AXIOMS:
            add_move_token(out_tokens, ltoken)

        elif name in ROTATION_TOKENS:
            ltoken: Any
            add_rotation_token(out_tokens, ltoken)

        elif name in BRUSH_TOKENS:
            pass

        # Enum Based Tokens
        elif name in STACK_TOKENS:
            add_stack_token(out_tokens, ltoken)

        elif name in PEN_TOKENS:
            add_pen_token(out_tokens, ltoken)

    # out_tokens[1:] to remove the left padding
    return out_tokens[1:]

# A[][1]--A
# A[1]-(2)A
